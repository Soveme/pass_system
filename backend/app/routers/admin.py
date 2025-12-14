from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from datetime import datetime

from app.database import get_db
from app.models.pass_model import Pass, PassStatus, Visit
from app.models.user import User, UserRole
from app.schemas.pass_schema import PassResponse, VisitResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Simple role check
async def check_admin_role(db: AsyncSession, user_id: int):
    """Check if user has admin role"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or user.role not in [UserRole.ADMIN, UserRole.MANAGEMENT]:
        raise HTTPException(status_code=403, detail="Access denied")
    return user

@router.get("/passes/search", response_model=list[PassResponse])
async def search_passes(
    db: AsyncSession = Depends(get_db),
    name: str = Query(None),
    company: str = Query(None),
    status_filter: PassStatus = Query(None),
    date_from: datetime = Query(None),
    date_to: datetime = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """Search passes with filters"""
    query = select(Pass)
    filters = []
    
    if name:
        filters.append(Pass.guest_name.ilike(f"%{name}%"))
    if company:
        filters.append(Pass.guest_company.ilike(f"%{company}%"))
    if status_filter:
        filters.append(Pass.status == status_filter)
    if date_from:
        filters.append(Pass.created_at >= date_from)
    if date_to:
        filters.append(Pass.created_at <= date_to)
    
    if filters:
        query = query.where(and_(*filters))
    
    result = await db.execute(query.offset(skip).limit(limit))
    passes = result.scalars().all()
    
    return [PassResponse.from_orm(p) for p in passes]

@router.get("/statistics")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    """Get system statistics"""
    # Total passes
    passes_result = await db.execute(select(Pass))
    total_passes = len(passes_result.scalars().all())
    
    # Active passes
    active_result = await db.execute(
        select(Pass).where(Pass.status == PassStatus.ACTIVE)
    )
    active_passes = len(active_result.scalars().all())
    
    # Total visits
    visits_result = await db.execute(select(Visit))
    total_visits = len(visits_result.scalars().all())
    
    # Today's visits
    today = datetime.utcnow().date()
    today_visits_result = await db.execute(
        select(Visit).where(Visit.entry_time >= datetime.combine(today, datetime.min.time()))
    )
    today_visits = len(today_visits_result.scalars().all())
    
    return {
        "total_passes": total_passes,
        "active_passes": active_passes,
        "expired_passes": total_passes - active_passes,
        "total_visits": total_visits,
        "today_visits": today_visits,
        "timestamp": datetime.utcnow()
    }

@router.get("/visits/log")
async def get_visits_log(
    db: AsyncSession = Depends(get_db),
    date_from: datetime = Query(None),
    date_to: datetime = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """Get visits log"""
    query = select(Visit)
    filters = []
    
    if date_from:
        filters.append(Visit.entry_time >= date_from)
    if date_to:
        filters.append(Visit.entry_time <= date_to)
    
    if filters:
        query = query.where(and_(*filters))
    
    result = await db.execute(
        query.order_by(Visit.entry_time.desc()).offset(skip).limit(limit)
    )
    visits = result.scalars().all()
    
    return [VisitResponse.from_orm(v) for v in visits]
