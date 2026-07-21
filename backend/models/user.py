from sqlalchemy import Column, String, Boolean
from models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    supabase_user_id = Column(String, unique=True, nullable=False, index=True)
