from typing import Optional
from sqlalchemy.orm import Session
from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_supabase_id(self, supabase_user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.supabase_user_id == supabase_user_id).first()
