from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional, Any, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.repositories.redis_repository import RedisRepository


class PasswordHelper:
    """
    Класс для работы с паролями: хеширование и верификация
    """
    def __init__(self):
        """ Инициализация контекста шифрования паролей """
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """ Хеширование пароля """
        return self._pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """ Проверка исходного пароля, используя хешированный пароль из БД """
        return self._pwd_context.verify(plain_password, hashed_password)


class JWTHelper:
    """
    Класс для работы с JWT токенами: создание, декодирование
    """
    def __init__(self):
        """ Инициализация с настройками из конфигурации """
        self._secret_key = settings.SECRET_KEY
        self._algorithm = settings.ALGORITHM
        self._access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_token_expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    def create_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """ Создание JWT токена """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(15)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encode_jwt

    def create_access_token(self, data: Dict[str, Any]) -> str:
        """
        Создание токена доступа
        data: Данные для кодирования (обычно sub и user_id)
        """
        expires_delta = timedelta(minutes=self._access_token_expire_minutes)
        return self.create_token(data=data, expires_delta=expires_delta)

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """ Создание токена обновления с более длительным временем жизни """
        expires_delta = timedelta(minutes=self._refresh_token_expire_minutes)
        return self.create_token(data=data, expires_delta=expires_delta)

    def create_pair_tokens(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> Dict[str, str]:
        """ Создание пары токенов: доступ и обвления """
        return {
            "access_token": self.create_token(data, expires_delta),
            "refresh_token": self.create_refresh_token(data),
            "token_type": "bearer"
        }

    def decode_token(self, token: str) -> Dict[str, Any]:
        """ Декодирование и проверка JWT токена """
        return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])


class TokenVerifier:
    """
    Класс для проверки токенов с инъекцией зависимости и кэшированием в Redis
    """
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    def __init__(
        self,
        jwt_helper: JWTHelper = JWTHelper(),
        cache_repo: RedisRepository= RedisRepository()
    ):
        self.jwt_helper = jwt_helper
        self.cache_repo = cache_repo

    async def __call__(self, token: str = Depends(oauth2_scheme)):
        """
        Проверка и декодирование токена
        и кэширование результатов в Redis
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось проверить учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

        # Проверка наличия кэша в Redis
        cached_data = self.cache_repo.get_cached_token(token)
        if cached_data:
            return cached_data

        try:
            # Декодирование токена
            payload = self.jwt_helper.decode_token(token)
            user_id = payload.get("sub")
            if user_id is None:
                raise credentials_exception

            # Кэширование результата в Redis с TTL равным оставшемуся времени жизни токена
            # Но не более чем на 1 час
            exp_time = payload.get("exp", 0)
            current_time = datetime.utcnow().timestamp()
            ttl = min(int(exp_time - current_time), 3600)

            if ttl > 0:
                token_data = {"user_id": user_id, "payload": payload}
                self.cache_repo.cache_token(token, token_data, ttl)

            return {"user_id": user_id, "payload": payload}

        except JWTError:
            raise credentials_exception
