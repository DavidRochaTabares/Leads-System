from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional, List


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str


class ProspectingSessionLogResponse(BaseModel):
    id: UUID
    level: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class ProspectingSessionCreate(BaseModel):
    industry: str
    location: str
    max_companies: int


class ProspectingSessionResponse(BaseModel):
    id: UUID
    industry: str
    location: str
    max_companies: int
    status: str
    progress: int
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProspectingSessionListResponse(BaseModel):
    sessions: List[ProspectingSessionResponse]

