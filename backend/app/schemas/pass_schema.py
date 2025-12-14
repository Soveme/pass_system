from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.pass_model import PassStatus

class PassCreate(BaseModel):
    guest_name: str
    guest_company: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_email: Optional[str] = None
    valid_from: datetime
    valid_until: datetime
    notes: Optional[str] = None

class PassUpdate(BaseModel):
    status: Optional[PassStatus] = None
    guest_company: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_email: Optional[str] = None
    valid_until: Optional[datetime] = None
    notes: Optional[str] = None

class PassResponse(BaseModel):
    id: int
    uuid: str
    qr_code: str
    guest_name: str
    guest_company: Optional[str]
    guest_phone: Optional[str]
    guest_email: Optional[str]
    status: PassStatus
    valid_from: datetime
    valid_until: datetime
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class VisitResponse(BaseModel):
    id: int
    pass_id: int
    entry_time: datetime
    exit_time: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
