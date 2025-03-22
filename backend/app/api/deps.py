from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Database
from app.core.utils.auth_service import AuthService
from app.core.utils.vacancy_service import VacancyService
from app.db.models import User
from app.exceptions.auth_exceptions import InactiveUserException, TokenValidationException
from app.core.security import TokenVerifier, JWTHelper
from app.repositories.user_repository import UserRepository
from app.repositories.redis_repository import RedisRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_jwt_helper() -> JWTHelper:
    """Функция-зависимость для получения JWTHelper"""
    return JWTHelper()


def get_redis_repo() -> RedisRepository:
    """Функция-зависимость для получения репозитория кэша токенов"""
    return RedisRepository()


def get_token_verifier() -> TokenVerifier:
    """ Функция-зависимость для использования верификатора токена """
    jwt_helper = get_jwt_helper()
    redis_repo = get_redis_repo()
    return TokenVerifier(jwt_helper, redis_repo)


async def get_user_repository(db: AsyncSession = Depends(Database.get_db)) -> UserRepository:
    """Функция-зависимость для получения репозитория пользователей"""
    return UserRepository(db)


async def get_auth_service(
    db: AsyncSession = Depends(Database.get_db),
    user_repo: UserRepository = Depends(get_user_repository),
    jwt_helper: JWTHelper = Depends(get_jwt_helper),
    token_verifier: TokenVerifier = Depends(get_token_verifier),
    redis_repo: RedisRepository = Depends(get_redis_repo)
) -> AuthService:
    """ Функция-зависимость для получения экземпляра AuthService """
    return AuthService(db, user_repo, None, jwt_helper, token_verifier, redis_repo)


async def get_token_data(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service)
):
    """ Функция-зависимость для получения данных токена с использованием AuthService """
    try:
        user = await auth_service.get_current_user_with_token(token)
        if not user:
            raise TokenValidationException()

        return {"payload": {"user_id": user.id}}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Не удалось проверить учетные данные: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user(
        token_data = Depends(get_token_data),
        auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """ Функция-зависимость для получения текущего пользователя """
    try:
        user_id = token_data.get("payload", {}).get("user_id")
        if not user_id:
            raise TokenValidationException()

        # Получаем пользователя из репозитория или кэша
        user = await auth_service._user_repo.get_by_id(user_id)
        if not user:
            raise TokenValidationException()

        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """ Функция-зависимость для получения активного пользователя """
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user


async def get_vacancy_service(db: AsyncSession = Depends(Database.get_db)) -> VacancyService:
    """ Функция-зависимость для получения экземпляра VacancyService """
    return VacancyService(db)
