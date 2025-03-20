from typing import Dict
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.db.models import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.core.security import PasswordHelper, JWTHelper
from app.exceptions.auth_exceptions import UserExistsException, InvalidCredentialsException, TokenValidationException, InactiveUserException


class AuthService:
    """
    Сервис аутентификации
    Логика для работы с пользователями и токенами, используя репозиторий для доступа к данным
    """
    def __init__(self, session: AsyncSession):
        """ Инициализация с сессией БД и вспомогательными классами """
        self._session = session
        self._user_repo = UserRepository(session)
        self._pwd_helper = PasswordHelper()
        self._jwt_helper = JWTHelper()

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """ Регистрация нового пользователя """
        if await self._user_repo.get_by_username(user_data.username):
            raise UserExistsException()

        hashed_password = self._pwd_helper.hash_password(user_data.password)
        user = await self._user_repo.create({
            "username": user_data.username,
            "hashed_password": hashed_password,
            "is_active": False
        })

        await self._session.commit()

        return UserResponse(id=user.id, username=user.username, is_active=user.is_active)

    async def login_user(self, form_data: OAuth2PasswordRequestForm) -> Token:
        """ Аутентификация пользователя, выдача токенов """
        user = await self._user_repo.get_by_username(form_data.username)
        if not user or not self._pwd_helper.verify_password(form_data.password, user.hashed_password):
            raise InvalidCredentialsException

        # Активация пользователя
        if not user.is_active:
            await self._user_repo.update(user.id, {"is_active": True})
            await self._session.commit()

        # Генерация токенов
        tokens = self._jwt_helper.create_pair_tokens({"sub": user.username, "user_id": user.id})
        return Token(**tokens)

    async def logout_user(self, token: str) -> UserResponse:
        """ Выход пользователя - деактивация учетной записи """
        try:
            # Валидация токена
            payload = self._jwt_helper.decode_token(token)
            username = payload.get("sub")
            user_id = payload.get("user_id")

            user = await self._user_repo.get_by_id(user_id)
            if not user or user.username != username:
                raise TokenValidationException()

            if not user.is_active:
                raise InactiveUserException()

            await self._user_repo.update(user.id, {"is_active": False})
            await self._session.commit()

            return UserResponse(id=user.id, username=user.username, is_active=False)
        except JWTError:
            raise TokenValidationException()

    async def refresh_token(self, refresh_token: str) -> Dict[str, str]:
        """ Обновление токена доступа с использованием токена обновления """
        try:
            # Валидация токена обновления
            payload = self._jwt_helper.decode_token(refresh_token)
            username = payload.get("sub")
            user_id = payload.get("user_id")

            user = await self._user_repo.get_by_id(user_id)
            if not user or user.username != username:
                raise TokenValidationException()

            if not user.is_active:
                raise InactiveUserException()

            # Генерация нового токена доступа
            access_token = self._jwt_helper.create_access_token({"sub": user.username, "user_id": user.id})
            return {"access_token": access_token, "token_type": "bearer"}
        except JWTError:
            raise TokenValidationException()

    async def get_current_user_with_token(self, token: str) -> User:
        """ Получение текущего пользователя по токену """
        try:
            # Валидация токена
            payload = self._jwt_helper.decode_token(token)
            username = payload.get("sub")
            if username is None:
                raise TokenValidationException()

            # Получение пользователя
            user = await self._user_repo.get_by_username(username)
            if user is None:
                raise TokenValidationException()

            return user
        except JWTError:
            raise TokenValidationException()

    async def check_is_auth(self, token: str) -> bool:
        """ Проверка аутентификации пользователя """
        user = await self.get_current_user_with_token(token)
        return user.is_active
