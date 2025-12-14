from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
import uuid

from app.database import Base

class UserRole(str, PyEnum):
    GUEST = "guest"
    EMPLOYEE = "employee"
    GUARD = "guard"
    HR = "hr"
    ADMIN = "admin"
    IT_SPECIALIST = "it_specialist"
    MANAGEMENT = "management"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(20), nullable=True)
    username = Column(String(255), unique=True, index=True)
    full_name = Column(String(255))
    hashed_password = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.GUEST)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    passes = relationship("Pass", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
