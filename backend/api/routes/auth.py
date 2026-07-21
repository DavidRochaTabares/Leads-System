from fastapi import APIRouter, Depends
from api.schemas import UserResponse
from api.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
