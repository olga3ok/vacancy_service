from typing import Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.repositories.base_repository import BaseRepository


class UnitOfWork:
    """
    Класс Unit of Work для управления транзакциями и репозиториями
    """
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._repositories: Dict[str, BaseRepository] = {}

    async def __aenter__(self):
        """ Создание асинхронной сессии при входе в контекст """
        self._session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """ Закрытие сессии и управление транзакцией при выходе из контекста """
        if exc_type is None:
            await self._session.commit()
        else:
            await self._session.rollback()
        await self._session.close()

    def get_repository(self, repository_class: Type[BaseRepository]) -> BaseRepository:
        """ Получение репозитория с использованием текущей сессии """
        if repository_class not in self._repositories:
            self._repositories[repository_class] = repository_class(self._session)
        return self._repositories[repository_class]

    @property
    def session(self) -> AsyncSession:
        """ Получение текущей сессии """
        if self._session is None:
            raise RuntimeError("UnitOfWork session not initialized")
        return self._session


class UnitOfWorkFactory:
    """ Фабрика для создания Unit Of Work """
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def create(self) -> UnitOfWork:
        """ Создание экземпляра Unit Of Work """
        return UnitOfWork(self._session_factory)
