from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.user import User, UserRole
from app.utils.security import hash_password

router = APIRouter(prefix="/api/demo", tags=["demo"])

@router.post("/create-demo-users")
async def create_demo_users(db: AsyncSession = Depends(get_db)):
    """
    Create demo users for testing purposes.
    Only works in development mode.
    """
    demo_users = [
        {
            "username": "admin",
            "password": "admin",
            "full_name": "Admin User",
            "email": "admin@example.com",
            "role": UserRole.ADMIN
        },
        {
            "username": "guard",
            "password": "guard",
            "full_name": "Guard User",
            "email": "guard@example.com",
            "role": UserRole.GUARD
        },
        {
            "username": "hr",
            "password": "hr",
            "full_name": "HR Manager",
            "email": "hr@example.com",
            "role": UserRole.HR
        },
        {
            "username": "manager",
            "password": "manager",
            "full_name": "Manager User",
            "email": "manager@example.com",
            "role": UserRole.MANAGEMENT
        }
    ]
    
    created = []
    skipped = []
    
    for user_data in demo_users:
        # Check if user already exists
        result = await db.execute(select(User).where(User.username == user_data["username"]))
        existing = result.scalar_one_or_none()
        
        if existing:
            skipped.append(user_data["username"])
            continue
        
        # Create new user
        user = User(
            username=user_data["username"],
            full_name=user_data["full_name"],
            email=user_data["email"],
            hashed_password=hash_password(user_data["password"]),
            role=user_data["role"],
            is_active=True
        )
        
        db.add(user)
        created.append(user_data["username"])
        
        print(f"[DEMO] Created user: {user_data['username']} with role: {user_data['role']}")
    
    await db.commit()
    
    return {
        "status": "success",
        "created": created,
        "skipped": skipped,
        "message": f"Created {len(created)} demo users. Skipped {len(skipped)} already existing."
    }

@router.get("/users")
async def get_demo_users():
    """
    Get list of demo users for testing
    """
    return {
        "demo_users": [
            {"username": "admin", "password": "admin", "role": "admin"},
            {"username": "guard", "password": "guard", "role": "guard"},
            {"username": "hr", "password": "hr", "role": "hr_manager"},
            {"username": "manager", "password": "manager", "role": "management"}
        ]
    }
