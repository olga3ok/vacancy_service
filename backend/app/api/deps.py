from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import TokenVerifier, JWTHelper, PasswordHelper
from app.db.base import Database
from app.db.models import User
from app.db.unit_of_work import UnitOfWork, UnitOfWorkFactory
from app.exceptions.auth_exceptions import InactiveUserException, TokenValidationException
from app.services.auth_service import AuthService
from app.repositories.redis_repository import RedisRepository
from app.services.vacancy_service import VacancyService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_unit_of_work_factory() -> UnitOfWorkFactory:
    """ Функция-зависимость для получения фабрики Unit of Work """
    return Database.get_unit_of_work_factory()


def get_unit_of_work(
        uow_factory: UnitOfWorkFactory = Depends(get_unit_of_work_factory)
) -> UnitOfWork:
    """ Функция-зависимость для получения Unit of Work """
    return uow_factory.create()


def get_jwt_helper() -> JWTHelper:
    """Функция-зависимость для получения JWTHelper"""
    return JWTHelper()


def get_password_helper() -> PasswordHelper:
    """ Функция-зависимость для получения PasswordHelper """
    return PasswordHelper()


def get_redis_repo() -> RedisRepository:
    """Функция-зависимость для получения репозитория кэша токенов"""
    return RedisRepository()


def get_token_verifier() -> TokenVerifier:
    """ Функция-зависимость для использования верификатора токена """
    jwt_helper = get_jwt_helper()
    redis_repo = get_redis_repo()
    return TokenVerifier(jwt_helper, redis_repo)


async def get_auth_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
    jwt_helper: JWTHelper = Depends(get_jwt_helper),
    token_verifier: TokenVerifier = Depends(get_token_verifier),
    redis_repo: RedisRepository = Depends(get_redis_repo)
) -> AuthService:
    """ Функция-зависимость для получения экземпляра AuthService """
    return AuthService(
        unit_of_work=uow,
        jwt_helper=jwt_helper,
        token_verifier=token_verifier,
        redis_repo=redis_repo)


async def get_token_data(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service)
):
    """ Функция-зависимость для получения данных токена с использованием AuthService """
    try:
        user = await auth_service.get_current_user_with_token(token)
        if not user:
            raise TokenValidationException()

        return {"payload": {"user_id": user.id, "token": token}}
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
        user = await auth_service.get_current_user_with_token(token_data.get("payload", {}).get("token", ""))
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


async def get_vacancy_service(uow: UnitOfWork = Depends(get_unit_of_work)) -> VacancyService:
    """ Функция-зависимость для получения экземпляра VacancyService """
    return VacancyService(uow)
