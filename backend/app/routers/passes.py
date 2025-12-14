from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
import uuid as uuid_lib

from app.database import get_db
from app.models.pass_model import Pass, PassStatus, Visit
from app.models.user import User
from app.schemas.pass_schema import PassCreate, PassUpdate, PassResponse, VisitResponse
from app.utils.qr_generator import generate_qr_code

router = APIRouter(prefix="/api/passes", tags=["passes"])

@router.post("/create", response_model=PassResponse)
async def create_pass(pass_data: PassCreate, db: AsyncSession = Depends(get_db)):
    """Create new pass for guest"""
    
    # Generate unique QR code
    qr_data = str(uuid_lib.uuid4())
    qr_base64, _ = generate_qr_code(qr_data)
    
    # Create pass
    new_pass = Pass(
        qr_code=qr_data,
        guest_name=pass_data.guest_name,
        guest_company=pass_data.guest_company,
        guest_phone=pass_data.guest_phone,
        guest_email=pass_data.guest_email,
        status=PassStatus.ACTIVE,
        valid_from=pass_data.valid_from,
        valid_until=pass_data.valid_until,
        notes=pass_data.notes
    )
    
    db.add(new_pass)
    await db.commit()
    await db.refresh(new_pass)
    
    print(f"[NOTIFICATION] Pass created for {pass_data.guest_name}")
    print(f"[EMAIL_STUB] Send email to {pass_data.guest_email}: Your pass is ready!")
    print(f"[SMS_STUB] Send SMS to {pass_data.guest_phone}: Your pass QR code: {qr_data}")
    
    return PassResponse.from_orm(new_pass)

@router.get("/", response_model=list[PassResponse])
async def list_passes(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    """List all passes"""
    result = await db.execute(select(Pass).offset(skip).limit(limit))
    passes = result.scalars().all()
    return [PassResponse.from_orm(p) for p in passes]

@router.get("/{pass_id}", response_model=PassResponse)
async def get_pass(pass_id: int, db: AsyncSession = Depends(get_db)):
    """Get pass by ID"""
    result = await db.execute(select(Pass).where(Pass.id == pass_id))
    pass_obj = result.scalar_one_or_none()
    
    if not pass_obj:
        raise HTTPException(status_code=404, detail="Pass not found")
    
    return PassResponse.from_orm(pass_obj)

@router.put("/{pass_id}", response_model=PassResponse)
async def update_pass(pass_id: int, pass_data: PassUpdate, db: AsyncSession = Depends(get_db)):
    """Update pass"""
    result = await db.execute(select(Pass).where(Pass.id == pass_id))
    pass_obj = result.scalar_one_or_none()
    
    if not pass_obj:
        raise HTTPException(status_code=404, detail="Pass not found")
    
    # Update fields
    for field, value in pass_data.dict(exclude_unset=True).items():
        setattr(pass_obj, field, value)
    
    await db.commit()
    await db.refresh(pass_obj)
    
    return PassResponse.from_orm(pass_obj)

@router.post("/{pass_id}/visit/entry")
async def record_entry(pass_id: int, db: AsyncSession = Depends(get_db)):
    """Record guest entry"""
    result = await db.execute(select(Pass).where(Pass.id == pass_id))
    pass_obj = result.scalar_one_or_none()
    
    if not pass_obj:
        raise HTTPException(status_code=404, detail="Pass not found")
    
    # Check if pass is valid
    now = datetime.utcnow()
    if pass_obj.status != PassStatus.ACTIVE or now > pass_obj.valid_until:
        raise HTTPException(status_code=403, detail="Pass is not valid")
    
    # Check if already entered (active visit)
    active_visit_result = await db.execute(
        select(Visit).where(
            Visit.pass_id == pass_id,
            Visit.exit_time == None
        )
    )
    active_visit = active_visit_result.scalar_one_or_none()
    
    if active_visit:
        return {"status": "already_entered", "visit_id": active_visit.id}
    
    # Create visit record
    visit = Visit(
        pass_id=pass_id,
        entry_time=now
    )
    
    db.add(visit)
    await db.commit()
    await db.refresh(visit)
    
    print(f"[AUDIT] Guest {pass_obj.guest_name} entered at {now}")
    
    return {
        "status": "success",
        "visit_id": visit.id,
        "entry_time": visit.entry_time
    }

@router.post("/{pass_id}/visit/exit")
async def record_exit(pass_id: int, db: AsyncSession = Depends(get_db)):
    """Record guest exit"""
    result = await db.execute(select(Pass).where(Pass.id == pass_id))
    pass_obj = result.scalar_one_or_none()
    
    if not pass_obj:
        raise HTTPException(status_code=404, detail="Pass not found")
    
    # Find active visit
    active_visit_result = await db.execute(
        select(Visit).where(
            Visit.pass_id == pass_id,
            Visit.exit_time == None
        )
    )
    active_visit = active_visit_result.scalar_one_or_none()
    
    if not active_visit:
        raise HTTPException(status_code=404, detail="No active visit found")
    
    # Record exit
    now = datetime.utcnow()
    active_visit.exit_time = now
    
    await db.commit()
    await db.refresh(active_visit)
    
    print(f"[AUDIT] Guest {pass_obj.guest_name} exited at {now}")
    
    return {
        "status": "success",
        "visit_id": active_visit.id,
        "exit_time": active_visit.exit_time
    }
