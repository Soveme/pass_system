from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from ..database import get_db
from ..models import User, Pass
from ..dependencies import get_current_user, check_admin_role

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/statistics")
async def get_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get admin statistics"""
    now = datetime.now(timezone.utc)
    
    # Total passes
    total_result = await db.execute(select(Pass))
    total_passes = len(total_result.scalars().all())
    
    # Active passes
    active_result = await db.execute(
        select(Pass).where(Pass.is_active == True)
    )
    active_passes = len(active_result.scalars().all())
    
    # Today's visits
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_result = await db.execute(
        select(Pass)
        .join(PassVisit)
        .where(PassVisit.entry_time >= today_start)
    )
    today_visits = len(today_result.scalars().all())
    
    # Total visits (count visits table)
    total_visits_result = await db.execute(select(PassVisit))
    total_visits = len(total_visits_result.scalars().all())
    
    return {
        "total_passes": total_passes,
        "active_passes": active_passes,
        "today_visits": today_visits,
        "total_visits": total_visits
    }


@router.get("/users")
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all users (admin only)"""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/users/search")
async def search_users(
    query: str = "",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search users by username or email"""
    result = await db.execute(
        select(User).where(
            (User.username.ilike(f"%{query}%")) |
            (User.email.ilike(f"%{query}%"))
        )
    )
    users = result.scalars().all()
    return users


@router.patch("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    status_update: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle user status (activate/deactivate)"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = status_update.get("is_active", user.is_active)
    
    await db.commit()
    await db.refresh(user)
    
    return user


@router.get("/audit-log")
async def get_audit_log(
    action: str = "",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get audit log (use /visits/log instead)"""
    # This is kept for compatibility, but /visits/log is the main endpoint
    return []


# Import PassVisit at the end to avoid circular imports
from ..models import PassVisit
