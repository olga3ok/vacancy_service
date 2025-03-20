from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timezone

from app.db.models import Vacancy


class VacancyRepository:
    """
    Репозиторий для работы с вакансиями.
    Инкапсулирует все операции с базой данных, связанные с моделью Vacancy
    """
    def __init__(self, session: AsyncSession):
        self._session = session


    async def create(self, vacancy_data: Dict[str, Any]) -> Vacancy:
        """ Создание новой вакансии """
        vacancy = Vacancy(**vacancy_data)
        self._session.add(vacancy)
        await self._session.flush()
        return vacancy

    async def get_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        """ Получение вакансии по ID """
        stmt = select(Vacancy).where(Vacancy.id == vacancy_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_by_hh_id(self, hh_id: str) -> Optional[Vacancy]:
        """ Получение вакансии по ID с HH.ru """
        stmt = select(Vacancy).where(Vacancy.hh_id == hh_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def update(self, vacancy_id: int, update_data: Dict[str, Any]) -> Optional[Vacancy]:
        """ Обновление данных вакансии """
        vacancy = await self.get_by_id(vacancy_id)
        if vacancy:
            # Дата обновления
            update_data["updated_at"] = datetime.now(timezone.utc)

            for key, value in update_data.items():
                if hasattr(vacancy, key) and value is not None:
                    setattr(vacancy, key, value)

            await self._session.flush()
        return vacancy

    async def delete(self, vacancy_id: int) -> bool:
        """ Удаление вакансии по ID """
        vacancy = await self.get_by_id(vacancy_id)
        if vacancy:
            await self._session.delete(vacancy)
            await self._session.flush()
            return True
        return False

    async def get_list(self, skip: int = 0, limit: int = 100) -> List[Vacancy]:
        """ Получение списка вакансий с поддержкой пагинации """
        stmt = select(Vacancy).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
