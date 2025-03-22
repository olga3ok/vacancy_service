import redis
import json
from typing import Optional, Dict

from app.core.config import settings


class RedisRepository:
    """
    Репозиторий для работы с Redis кэшем
    """
    def __init__(self, redis_client=None):
        self.redis_client = redis_client or redis.Redis.from_url(settings.REDIS_URL)

    # Общие методы
    def get_cached_item(self, prefix: str, item_id: str) -> Optional[Dict]:
        """Получение закэшированного объекта"""
        cache_key = f"{prefix}:{item_id}"
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        return None

    def cache_item(self, prefix: str, item_id: str, data: Dict, ttl: int) -> None:
        """Кэширование объекта"""
        cache_key = f"{prefix}:{item_id}"
        if ttl > 0:
            self.redis_client.setex(
                cache_key,
                ttl,
                json.dumps(data)
            )
        else:
            self.redis_client.set(cache_key, json.dumps(data))

    def delete_cache(self, prefix: str, item_id: str) -> None:
        """Удаление кэша объекта"""
        cache_key = f"{prefix}:{item_id}"
        self.redis_client.delete(cache_key)

    # Методы для работы с токенами
    def get_cached_token(self, token: str) -> Optional[Dict]:
        """Получение закэшированного токена"""
        return self.get_cached_item("token", token)

    def cache_token(self, token: str, data: Dict, ttl: int) -> None:
        """Кэширование токена"""
        self.cache_item("token", token, data, ttl)

    def delete_token_cache(self, token: str) -> None:
        """Удаление кэша токена"""
        self.delete_cache("token", token)

    # Методы для работы с пользователями
    def get_cached_user(self, user_id: int) -> Optional[Dict]:
        """Получение закэшированного пользователя"""
        return self.get_cached_item("user", str(user_id))

    def cache_user(self, user_id: int, user_data: Dict, ttl: int) -> None:
        """Кэширование данных пользователя"""
        self.cache_item("user", str(user_id), user_data, ttl)

    def delete_user_cache(self, user_id: int) -> None:
        """Удаление кэша пользователя"""
        self.delete_cache("user", str(user_id))
