from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta

from ..database import get_db
from ..models import PassVisit, Pass, User
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/visits", tags=["visits"])


@router.get("/log")
async def get_visits_log(
    date: str = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get visits log with guest and pass information"""
    query = select(PassVisit).join(Pass).offset(skip).limit(limit)
    
    # Filter by date if provided
    if date:
        try:
            filter_date = datetime.strptime(date, "%Y-%m-%d")
            start = filter_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
            query = query.where(
                (PassVisit.visit_time >= start) &
                (PassVisit.visit_time < end)
            )
        except ValueError:
            pass
    
    result = await db.execute(query.order_by(PassVisit.visit_time.desc()))
    visits = result.scalars().all()
    
    # Format response with guest and pass information
    response = []
    for visit in visits:
        pass_obj = await db.get(Pass, visit.pass_id)
        guard = await db.get(User, visit.guard_id)
        
        response.append({
            "id": visit.id,
            "visit_time": visit.visit_time,
            "guest_name": pass_obj.guest_name if pass_obj else "Unknown",
            "guest_company": pass_obj.guest_company if pass_obj else "Unknown",
            "pass_uuid": pass_obj.uuid if pass_obj else "Unknown",
            "guard_username": guard.username if guard else "Unknown"
        })
    
    return response
