from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
import uuid

from app.database import Base

class PassStatus(str, PyEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    PENDING = "pending"

class Pass(Base):
    __tablename__ = "passes"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    qr_code = Column(String(500), unique=True, index=True)
    guest_name = Column(String(255), index=True)
    guest_company = Column(String(255), nullable=True, index=True)
    guest_phone = Column(String(20), nullable=True)
    guest_email = Column(String(255), nullable=True, index=True)
    guest_photo_url = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(PassStatus), default=PassStatus.PENDING, index=True)
    valid_from = Column(DateTime(timezone=True))
    valid_until = Column(DateTime(timezone=True))
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    user = relationship("User", back_populates="passes")
    visits = relationship("Visit", back_populates="pass_obj")
    
class Visit(Base):
    __tablename__ = "visits"
    
    id = Column(Integer, primary_key=True, index=True)
    pass_id = Column(Integer, ForeignKey("passes.id"), index=True)
    entry_time = Column(DateTime(timezone=True))
    exit_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    pass_obj = relationship("Pass", back_populates="visits")
