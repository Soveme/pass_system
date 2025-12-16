from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.user import User, UserRole
from app.utils.security import verify_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        print(f"[SECURITY] Invalid token used")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("id")
    if not user_id:
        print(f"[SECURITY] Token missing user id")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        print(f"[SECURITY] User not found: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        print(f"[SECURITY] Inactive user attempt: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    
    return user

async def check_admin_role(user: User = Depends(get_current_user)):
    """Check if user has admin role"""
    
    if user.role not in [UserRole.ADMIN, UserRole.IT_SPECIALIST, UserRole.MANAGEMENT]:
        print(f"[SECURITY] Non-admin user tried to access admin resource: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return user

async def check_guard_role(user: User = Depends(get_current_user)):
    """Check if user has guard role"""
    
    if user.role not in [UserRole.GUARD, UserRole.ADMIN, UserRole.HR]:
        print(f"[SECURITY] Non-guard user tried to scan pass: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Guard access required"
        )
    
    return user
