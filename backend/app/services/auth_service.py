from typing import Dict, Optional
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from datetime import datetime

from app.core.security import PasswordHelper, JWTHelper, TokenVerifier
from app.db.models import User
from app.db.unit_of_work import UnitOfWork
from app.exceptions.auth_exceptions import (
    UserExistsException,
    InvalidCredentialsException,
    TokenValidationException,
    InactiveUserException
)
from app.repositories.redis_repository import RedisRepository
from app.repositories.user_repository import UserRepository
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse


class AuthService:
    """
    Сервис аутентификации
    Логика для работы с пользователями и токенами, используя репозиторий для доступа к данным
    с поддержкой кэширования в Redis
    """
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        pwd_helper: Optional[PasswordHelper] = None,
        jwt_helper: Optional[JWTHelper] = None,
        token_verifier: Optional[TokenVerifier] = None,
        redis_repo: Optional[RedisRepository] = None
    ):
        """ Инициализация с сессией БД и вспомогательными классами """
        self._uow = unit_of_work
        self._pwd_helper = pwd_helper or PasswordHelper()
        self._jwt_helper = jwt_helper or JWTHelper()
        self._token_verifier = token_verifier or TokenVerifier(self._jwt_helper)
        self._redis_repo = redis_repo or RedisRepository()

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """ Регистрация нового пользователя """
        async with self._uow:
            user_repo = self._uow.get_repository(UserRepository)

            existing_user = await user_repo.get_by_username(user_data.username)
            if existing_user:
                raise UserExistsException()

            hashed_password = self._pwd_helper.hash_password(user_data.password)
            user = await user_repo.create({
                "username": user_data.username,
                "hashed_password": hashed_password,
                "is_active": False
            })

            return UserResponse(
                id=user.id,
                username=user.username,
                is_active=user.is_active
            )

    async def login_user(self, form_data: OAuth2PasswordRequestForm) -> Token:
        """ Аутентификация пользователя, выдача токенов """
        async with self._uow:
            user_repo = self._uow.get_repository(UserRepository)

            user = await user_repo.get_by_username(form_data.username)
            if not user or not self._pwd_helper.verify_password(form_data.password, user.hashed_password):
                raise InvalidCredentialsException

            # Активация пользователя
            if not user.is_active:
                await user_repo.update(user.id, {"is_active": True})

            # Генерация токенов
            tokens = self._jwt_helper.create_pair_tokens({"sub": user.username, "user_id": user.id})

            # Кэширование в Redis информации о пользователе и токене для быстрого доступа
            access_payload = self._jwt_helper.decode_token(tokens["access_token"])
            self._cache_user_token_info(user, access_payload)

            return Token(**tokens)

    async def logout_user(self, token: str) -> UserResponse:
        """ Выход пользователя - деактивация учетной записи """
        async with self._uow:
            user_repo = self._uow.get_repository(UserRepository)

            try:
                # Валидация токена
                payload = self._jwt_helper.decode_token(token)
                username = payload.get("sub")
                user_id = payload.get("user_id")

                user = await user_repo.get_by_id(user_id)
                if not user or user.username != username:
                    raise TokenValidationException()

                if not user.is_active:
                    raise InactiveUserException()

                await user_repo.update(user.id, {"is_active": False})

                # Удаление кэша токена и пользователя
                self._redis_repo.delete_token_cache(token)
                self._redis_repo.delete_user_cache(user.id)

                return UserResponse(
                    id=user.id,
                    username=user.username,
                    is_active=False
                )
            except JWTError:
                raise TokenValidationException()

    async def refresh_token(self, refresh_token: str) -> Dict[str, str]:
        """ Обновление токена доступа с использованием токена обновления """
        async with self._uow:
            user_repo = self._uow.get_repository(UserRepository)

            try:
                # Валидация токена обновления
                payload = self._jwt_helper.decode_token(refresh_token)
                username = payload.get("sub")
                user_id = payload.get("user_id")

                user = await user_repo.get_by_id(user_id)
                if not user or user.username != username:
                    raise TokenValidationException()

                if not user.is_active:
                    raise InactiveUserException()

                # Генерация нового токена доступа
                access_token = self._jwt_helper.create_access_token({"sub": user.username, "user_id": user.id})

                # Кэширование информации о новом токене
                access_payload = self._jwt_helper.decode_token(access_token)
                self._cache_user_token_info(user, access_payload)

                return {"access_token": access_token, "token_type": "bearer"}
            except JWTError:
                raise TokenValidationException()

    async def get_current_user_with_token(self, token: str) -> User:
        """
        Получение текущего пользователя по токену
        с использованием кэша в Redis
        """
        async with self._uow:
            user_repo = self._uow.get_repository(UserRepository)

            try:
                # Проверка токена в JWT
                payload = self._jwt_helper.decode_token(token)
                user_id = payload.get("user_id")

                if not user_id:
                    raise TokenValidationException()

                # Проверка кэша пользователя в Redis
                cached_user = self._redis_repo.get_cached_user(user_id)
                if cached_user:
                    user = User(**cached_user)
                    return user

                # Если кэша нет - получение из БД
                user = await user_repo.get_by_id(user_id)
                if user is None:
                    raise TokenValidationException()

                # Кэширование результата
                self._cache_user_token_info(user, payload)

                return user
            except JWTError:
                raise TokenValidationException()

    async def check_is_auth(self, token: str) -> bool:
        """ Проверка аутентификации пользователя """
        user = await self.get_current_user_with_token(token)
        return user.is_active

    def _cache_user_token_info(self, user: User, payload: Dict) -> None:
        """ Кэширование данных пользователя в Redis """
        user_data = {
            "id": user.id,
            "username": user.username,
            "is_active": user.is_active,
            "hashed_password": user.hashed_password
        }

        exp_time = payload.get("exp", 0)
        current_time = datetime.utcnow().timestamp()
        ttl = min(int(exp_time - current_time), 3600)  # Не больше часа

        if ttl > 0:
            self._redis_repo.cache_user(user.id, user_data, ttl)
