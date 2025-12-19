from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timezone

from app.database import get_db
from app.models.pass_model import Pass, PassStatus, Visit
from app.models.user import User, UserRole
from app.schemas.pass_schema import VerifyPassRequest

router = APIRouter(prefix="/api/scan", tags=["scanning"])

@router.post("/verify")
async def verify_pass(request: VerifyPassRequest, db: AsyncSession = Depends(get_db)):
    """Verify QR code and check pass validity"""
    
    qr_code = request.qr_code
    # Find pass by QR code
    result = await db.execute(select(Pass).where(Pass.qr_code == qr_code))
    pass_obj = result.scalar_one_or_none()
    
    if not pass_obj:
        return {
            "status": "DENIED",
            "reason": "Pass not found",
            "guest_name": None,
            "is_valid": False
        }
    
    # Check if pass is active
    if not pass_obj.is_active:
        return {
            "status": "DENIED",
            "reason": "Pass is inactive",
            "guest_name": pass_obj.guest_name,
            "is_valid": False
        }
    
    now = datetime.now(timezone.utc)
    
    # Check validity dates
    if now < pass_obj.valid_from:
        return {
            "status": "DENIED",
            "reason": "Pass not yet valid",
            "guest_name": pass_obj.guest_name,
            "is_valid": False
        }
    
    if now > pass_obj.valid_until:
        # Auto-expire pass
        pass_obj.is_active = False
        await db.commit()
        
        return {
            "status": "DENIED",
            "reason": "Pass expired",
            "guest_name": pass_obj.guest_name,
            "is_valid": False
        }
    
    # Check if already entered
    active_visit_result = await db.execute(
        select(Visit).where(
            Visit.pass_id == pass_obj.id,
            Visit.exit_time == None
        ).order_by(Visit.id.desc()).limit(1)
    )
    active_visit = active_visit_result.scalar_one_or_none()
    
    if active_visit:
        active_visit.exit_time = now
    
        await db.commit()
        await db.refresh(active_visit)
        
        duration_minutes = int((now - active_visit.entry_time).total_seconds() / 60)
        
        print(f"[AUDIT] Check-out: {pass_obj.guest_name} at {now} (duration: {duration_minutes} min)")
        
        return {
            "status": "EXIT",
            "reason": "Valid pass",
            "guest_name": pass_obj.guest_name,
            "guest_company": pass_obj.guest_company,
            "guest_photo_url": getattr(pass_obj, 'guest_photo_url', None),
            "valid_until": pass_obj.valid_until,
            "pass_id": pass_obj.id,
            "duration_minutes": duration_minutes
        }
    
    # Record visit
    visit = Visit(
        pass_id=pass_obj.id,
        entry_time=now
    )
    db.add(visit)
    await db.commit()
    
    print(f"[AUDIT] Check-in: {pass_obj.guest_name} at {now}")
    
    return {
        "status": "ALLOWED",
        "reason": "Valid pass",
        "guest_name": pass_obj.guest_name,
        "guest_company": pass_obj.guest_company,
        "guest_photo_url": getattr(pass_obj, 'guest_photo_url', None),
        "valid_until": pass_obj.valid_until,
        "pass_id": pass_obj.id,
        "is_valid": True
    }

@router.post("/check-in")
async def check_in(pass_id: int, db: AsyncSession = Depends(get_db)):
    """Check in guest - record entry"""
    
    result = await db.execute(select(Pass).where(Pass.id == pass_id))
    pass_obj = result.scalar_one_or_none()
    
    if not pass_obj:
        raise HTTPException(status_code=404, detail="Pass not found")
    
    # Record entry via the existing endpoint logic
    now = datetime.now(timezone.utc)
    
    # Check if already entered
    active_visit_result = await db.execute(
        select(Visit).where(
            Visit.pass_id == pass_id,
            Visit.exit_time == None
        ).order_by(Visit.id.desc()).limit(1)
    )
    active_visit = active_visit_result.scalar_one_or_none()
    
    if active_visit:
        active_visit.exit_time = now
    
        await db.commit()
        await db.refresh(active_visit)
        
        duration_minutes = int((now - active_visit.entry_time).total_seconds() / 60)
        
        print(f"[AUDIT] Check-out: {pass_obj.guest_name} at {now} (duration: {duration_minutes} min)")
        
        return {
            "status": "EXIT",
            "reason": "Valid pass",
            "guest_name": pass_obj.guest_name,
            "guest_company": pass_obj.guest_company,
            "guest_photo_url": getattr(pass_obj, 'guest_photo_url', None),
            "valid_until": pass_obj.valid_until,
            "pass_id": pass_obj.id,
            "duration_minutes": duration_minutes
        }
    
    # Record visit
    visit = Visit(
        pass_id=pass_obj.id,
        entry_time=now
    )
    db.add(visit)
    await db.commit()
    
    print(f"[AUDIT] Check-in: {pass_obj.guest_name} at {now}")
    
    return {
        "status": "ALLOWED",
        "reason": "Valid pass",
        "guest_name": pass_obj.guest_name,
        "guest_company": pass_obj.guest_company,
        "guest_photo_url": getattr(pass_obj, 'guest_photo_url', None),
        "valid_until": pass_obj.valid_until,
        "pass_id": pass_obj.id,
        "is_valid": True
    }


@router.post("/check-out")
async def check_out(pass_id: int, db: AsyncSession = Depends(get_db)):
    """Check out guest - record exit"""
    
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
        return {
            "status": "not_checked_in",
            "message": f"Guest {pass_obj.guest_name} is not checked in"
        }
    
    now = datetime.now(timezone.utc)
    active_visit.exit_time = now
    
    await db.commit()
    await db.refresh(active_visit)
    
    duration_minutes = int((now - active_visit.entry_time).total_seconds() / 60)
    
    print(f"[AUDIT] Check-out: {pass_obj.guest_name} at {now} (duration: {duration_minutes} min)")
    
    return {
        "status": "success",
        "message": f"Goodbye {pass_obj.guest_name}!",
        "visit_id": active_visit.id,
        "exit_time": active_visit.exit_time,
        "duration_minutes": duration_minutes
    }
