from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.vacancy_repository import VacancyRepository
from app.schemas.vacancy import VacancyCreate, VacancyUpdate
from app.utils.hh_parser import HHParser


class VacancyService:
    """
    Сервис для работы с вакансиями
    Логика работы с вакансиями, используя репозиторий для доступа к данным
    """
    def __init__(self, session: AsyncSession):
        """ Инициализация с сессией БД и репозиторием """
        self._session = session
        self._vacancy_repo = VacancyRepository(session)

    async def create_vacancy(self, vacancy_data: Optional[VacancyCreate] = None, hh_id: Optional[str] = None) -> Dict[str, Any]:
        """ Создание вакансии из данных или путем парсинга с HH.ru """
        # Получение данных с HH.ru по ID
        if hh_id:
            try:
                vacancy_data = await HHParser.get_vacancy_from_hh(hh_id)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ошибка при получении вакансии с HH.ru: {str(e)}"
                )

        # Проверка наличия данных
        if not vacancy_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неоходимо предоставить либо данные вакансии, либо ID с HH.ru"
            )

        # Проверка существования вакансии с таким hh_id
        if vacancy_data.hh_id:
            existing_vacancy = await self._vacancy_repo.get_by_hh_id(vacancy_data.hh_id)
            if existing_vacancy:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Вакансия с ID {vacancy_data.hh_id} с HH.ru уже существует"
                )

        # Создание вакансии
        vacancy = await self._vacancy_repo.create(vacancy_data.dict())
        await self._session.commit()
        return vacancy

    async def update_vacancy(self, vacancy_id: int, vacancy_data: VacancyUpdate) -> Dict[str, Any]:
        """ Обновление данных вакансии """
        # Поиск вакансии
        db_vacancy = await self._vacancy_repo.get_by_id(vacancy_id)
        if not db_vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вакансия с ID {vacancy_id} не найдена"
            )

        # Обновление данных с HH.ru, если запрошено
        update_data = vacancy_data.dict(exclude_unset=True)
        if vacancy_data.hh_id and vacancy_data.hh_id != db_vacancy.hh_id:
            try:
                hh_data = await HHParser.get_vacancy_from_hh(vacancy_data.hh_id)
                hh_data_dict = hh_data.dict()

                # Обновляем только те поля, которые не были указаны в vacancy_data
                for key, value in hh_data_dict.items():
                    if key not in update_data or update_data[key] is None:
                        update_data[key] = value

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ошибка при получении вакансии с HH.ru: {str(e)}"
                )

        # Обновление вакансии
        updated_vacancy = await self._vacancy_repo.update(vacancy_id, update_data)
        await self._session.commit()
        return updated_vacancy

    async def get_vacancy(self, vacancy_id: int) -> Dict[str, Any]:
        """ Получение вакансии по ID """
        vacancy = await self._vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Вакансия с ID {vacancy_id} не найдена"
            )
        return vacancy

    async def delete_vacancy(self, vacancy_id: int) -> None:
        """ Удаление вакансии по ID """
        success = await self._vacancy_repo.delete(vacancy_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вакансия с ID {vacancy_id} не найдена"
            )
        await self._session.commit()

    async def refresh_vacancy_from_hh(self, vacancy_id: int) -> Dict[str, Any]:
        """ Обновление данных с вакансии из HH.ru по сохраненному hh_id"""
        vacancy = await self._vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вакансия с ID {vacancy_id} не найдена"
            )

        if not vacancy.hh_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Эта вакансия не имеет привязки к ID с HH.ru"
            )

        try:
            # Получение обновленных данных с HH.ru
            updated_data = await HHParser.get_vacancy_from_hh(vacancy.hh_id)
            updated_vacancy = await self._vacancy_repo.update(vacancy_id, updated_data.dict())
            await self._session.commit()
            return updated_vacancy

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при получении вакансии с HH.ru: {str(e)}"
            )

    async def get_vacancies_list(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """ Получение списка вакансий с поддержкой пагинации """
        vacancies = await self._vacancy_repo.get_list(skip, limit)
        return vacancies
