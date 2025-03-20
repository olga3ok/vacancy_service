from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Database
from app.core.utils.auth_service import AuthService
from app.core.utils.vacancy_service import VacancyService
from app.db.models import User
from app.exceptions.auth_exceptions import InactiveUserException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_auth_service(db: AsyncSession = Depends(Database.get_db)) -> AuthService:
    """ Функция-зависимость для получения экземпляра AuthService """
    return AuthService(db)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """ Функция-зависимость для получения текущего пользователя """
    return await auth_service.get_current_user_with_token(token)


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """ Функция-зависимость для получения активного пользователя """
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user


async def get_vacancy_service(db: AsyncSession = Depends(Database.get_db)) -> VacancyService:
    """ Функция-зависимость для получения экземпляра VacancyService """
    return VacancyService(db)
