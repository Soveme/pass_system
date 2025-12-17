from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    role: str = "user"


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PassCreate(BaseModel):
    guest_name: str
    guest_company: str
    guest_email: str
    guest_phone: str
    valid_from: datetime
    valid_until: datetime


class PassUpdate(BaseModel):
    guest_name: Optional[str] = None
    guest_company: Optional[str] = None
    valid_until: Optional[datetime] = None
    is_active: Optional[bool] = None


class PassResponse(BaseModel):
    id: int
    uuid: str
    qr_code: str
    guest_name: str
    guest_company: str
    guest_email: str
    guest_phone: str
    valid_from: datetime
    valid_until: datetime
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
