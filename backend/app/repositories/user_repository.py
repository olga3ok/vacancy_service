from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, Dict, Any

from app.db.models import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    """
    Репозиторий для работы с пользователями.
    Все операции с базой данных, связанные с моделью User
    """
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_username(self, username: str) -> Optional[User]:
        """ Получение пользователя по имени пользователя """
        stmt = select(User).where(User.username == username)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """ Получение пользователя по ID """
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def create(self, user_data: Dict[str, Any]) -> User:
        """ Создание нового пользователя """
        user = User(**user_data)
        self._session.add(user)
        await self._session.flush()
        return user

    async def update(self, user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
        """ Обновление данных пользователя """
        user = await self.get_by_id(user_id)
        if user:
            for key, value in update_data.items():
                setattr(user, key, value)
            await self._session.flush()
        return user

    async def delete(self, user_id: int) -> Optional[User]:
        """ Удаление пользователя """
        user = await self.get_by_id(user_id)
        if user:
            await self._session.delete(user)
            await self._session.flush()
        return user
