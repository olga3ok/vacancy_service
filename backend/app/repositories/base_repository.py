from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    """ Абстрактный базовый репозиторий для всех репозиториев """
    def __init__(self, session: AsyncSession):
        self._session = session

    @abstractmethod
    async def get_by_id(self, _id):
        """ Получение объекта по идентификатору """
        pass

    @abstractmethod
    async def create(self, data):
        """ Создание нового объекта """
        pass

    @abstractmethod
    async def update(self, _id, data):
        """ Обновление объекта """
        pass

    @abstractmethod
    async def delete(self, _id):
        """ Удаление объекта """
        pass
