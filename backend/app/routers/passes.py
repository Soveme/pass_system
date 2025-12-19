from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
import uuid

from ..database import get_db
from ..models import Pass, User
from ..schemas import PassResponse, PassCreate, PassUpdate, SendEmailRequest
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/passes", tags=["passes"])


@router.get("/", response_model=list[PassResponse])
async def get_passes(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all passes"""
    result = await db.execute(
        select(Pass).offset(skip).limit(limit)
    )
    passes = result.scalars().all()
    return passes


@router.post("/create", response_model=PassResponse)
async def create_pass(pass_data: PassCreate, db: AsyncSession = Depends(get_db)):
    """Create a new pass"""
    new_pass = Pass(
        uuid=str(uuid.uuid4()),
        qr_code=str(uuid.uuid4()),
        guest_name=pass_data.guest_name,
        guest_company=pass_data.guest_company,
        guest_email=pass_data.guest_email,
        guest_phone=pass_data.guest_phone,
        valid_from=pass_data.valid_from,
        valid_until=pass_data.valid_until,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    
    db.add(new_pass)
    await db.commit()
    await db.refresh(new_pass)
    
    # TODO: Send SMS and Email notifications
    print(f"[NOTIFICATION] Pass created and sent to email")
    print(f"[SMS] Pass sent to {new_pass.guest_phone}")
    
    return new_pass


@router.put("/{pass_id}", response_model=PassResponse)
async def update_pass(
    pass_id: int,
    pass_update: PassUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a pass (admin only)"""
    result = await db.execute(
        select(Pass).where(Pass.id == pass_id)
    )
    pass_obj = result.scalar_one_or_none()
    
    if not pass_obj:
        raise HTTPException(status_code=404, detail="Pass not found")
    
    # Update fields if provided
    if pass_update.guest_name is not None:
        pass_obj.guest_name = pass_update.guest_name
    if pass_update.guest_company is not None:
        pass_obj.guest_company = pass_update.guest_company
    if pass_update.guest_phone is not None:
        pass_obj.guest_phone = pass_update.guest_phone
    if pass_update.guest_email is not None:
        pass_obj.guest_email = pass_update.guest_email
    if pass_update.valid_until is not None:
        pass_obj.valid_until = pass_update.valid_until
    if pass_update.is_active is not None:
        pass_obj.is_active = pass_update.is_active
    
    await db.commit()
    await db.refresh(pass_obj)
    
    return pass_obj


@router.delete("/{pass_id}")
async def delete_pass(
    pass_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a pass (admin only)"""
    result = await db.execute(
        select(Pass).where(Pass.id == pass_id)
    )
    pass_obj = result.scalar_one_or_none()
    if not pass_obj:
        raise HTTPException(status_code=404, detail="Pass not found")
    
    await db.delete(pass_obj)
    await db.commit()
    
    return {"status": "success", "message": "Pass deleted"}


@router.get("/search")
async def search_passes(
    name: str = "",
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search passes by name (admin only)"""
    result = await db.execute(
        select(Pass)
        .where(
            or_(
                Pass.guest_name.ilike(f"%{name}%"),
                Pass.guest_email.ilike(f"%{name}%"),
                Pass.guest_company.ilike(f"%{name}%"),
                Pass.guest_phone.ilike(f"%{name}%"),
                Pass.uuid.ilike(f"%{name}%")  # Поиск по ID пропуска
            )
        )
        .offset(skip)
        .limit(limit)
    )
    passes = result.scalars().all()
    return passes


@router.post("/{pass_id}/send-email")
async def send_email_to_pass(
    pass_id: int,
    email_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send email to guest"""
    pass_obj = await db.get(Pass, pass_id)
    if not pass_obj:
        raise HTTPException(status_code=404, detail="Pass not found")
    
    message = email_data.get("message", "")
    recipient_email = email_data.get("recipient_email", pass_obj.guest_email)
    
    # ЗАГЛУШКА - выводим в терминал
    print(f"╔════════════════════════════════════════════════╗")
    print(f"║ EMAIL SENT                                     ║")
    print(f"╠════════════════════════════════════════════════╣")
    print(f"║ To: {recipient_email}")
    print(f"║ Guest: {pass_obj.guest_name}")
    print(f"║ Pass ID: {pass_obj.uuid}")
    print(f"╠════════════════════════════════════════════════╣")
    print(f"║ MESSAGE:")
    print(f"║ {message}")
    print(f"╚════════════════════════════════════════════════╝")
    
    # TODO: Реально отправить письмо через SMTP
    
    return {
        "status": "success",
        "message": "Email sent successfully",
        "pass_id": pass_id,
        "recipient": recipient_email
    }
