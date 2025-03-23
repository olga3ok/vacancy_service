from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db.models import User
from app.schemas.token import Token
from app.schemas.user import UserResponse, UserCreate
from app.services.auth_service import AuthService
from app.api.deps import get_auth_service, oauth2_scheme, get_current_active_user


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """ Регистрация нового пользователя """
    return await auth_service.register_user(user_data)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """ Аутентификация пользователя и получение токенов """
    return await auth_service.login_user(form_data)


@router.post("/logout", response_model=UserResponse)
async def logout(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
):
    """ Выход пользователя (деактивация) """
    return await auth_service.logout_user(token)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """ Обновление токена доступа """
    token_data = await auth_service.refresh_token(refresh_token)
    return Token(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        refresh_token=refresh_token
    )


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """ Получение информации о текущем пользователе. """
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        is_active=current_user.is_active
    )
