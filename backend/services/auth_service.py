from typing import Optional
from sqlalchemy.orm import Session
from supabase import Client
from models.user import User
from repositories.user_repository import UserRepository
from core.exceptions import AuthenticationError


class AuthService:
    def __init__(self, db: Session, supabase: Client):
        self.db = db
        self.supabase = supabase
        self.user_repo = UserRepository(db)
    
    async def verify_token(self, token: str) -> User:
        try:
            print(f"[AUTH] Verifying token...")
            user_response = self.supabase.auth.get_user(token)
            print(f"[AUTH] Supabase response: {user_response}")
            
            if not user_response or not user_response.user:
                print(f"[AUTH] No user in response")
                raise AuthenticationError("Invalid token")
            
            supabase_user = user_response.user
            print(f"[AUTH] Supabase user ID: {supabase_user.id}, email: {supabase_user.email}")
            
            user = self.user_repo.get_by_supabase_id(supabase_user.id)
            print(f"[AUTH] Local user found: {user is not None}")
            
            if not user:
                print(f"[AUTH] Creating new user...")
                user = User(
                    email=supabase_user.email,
                    supabase_user_id=supabase_user.id,
                    full_name=supabase_user.user_metadata.get("full_name"),
                    is_active=True
                )
                user = self.user_repo.create(user)
                print(f"[AUTH] User created: {user.id}")
            
            print(f"[AUTH] Returning user: {user.id}")
            return user
            
        except Exception as e:
            print(f"[AUTH] Error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise AuthenticationError(f"Authentication failed: {str(e)}")
    
    def get_current_user(self, token: str) -> Optional[User]:
        try:
            user_response = self.supabase.auth.get_user(token)
            if user_response and user_response.user:
                return self.user_repo.get_by_supabase_id(user_response.user.id)
        except:
            pass
        return None
