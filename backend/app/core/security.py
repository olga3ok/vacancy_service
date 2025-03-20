from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from typing import Optional, Any, Dict

from app.core.config import settings


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
