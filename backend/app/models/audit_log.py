from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
import json

from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), index=True)  # CREATE, READ, UPDATE, DELETE
    entity_type = Column(String(100), index=True)  # Pass, User, Visit
    entity_id = Column(String(36), nullable=True)
    changes = Column(Text, nullable=True)  # JSON with before/after values
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    user = relationship("User", back_populates="audit_logs")
