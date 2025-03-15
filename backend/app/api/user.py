from fastapi import APIRouter, Depends, HTTPException

from app.db.models import User
from app.api.auth import get_current_active_user
from app.schemas.user import UserResponse


router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Получение имени текущего авторизованного пользователя
    """
    return {"username": current_user.username}