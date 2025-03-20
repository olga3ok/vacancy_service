from fastapi import APIRouter, Depends, status

from app.core.utils.vacancy_service import VacancyService
from app.api.deps import get_current_active_user, get_vacancy_service
from app.db.models import User
from app.schemas.vacancy import VacancyCreate, Vacancy as VacancySchema, VacancyUpdate


router = APIRouter()


@router.post("/create", response_model=VacancySchema)
async def create_vacancy(
    vacancy_data: VacancyCreate = None,
    hh_id: str = None,
    current_user: User = Depends(get_current_active_user),
    vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    """
    Создание вакансии:
    - Либо из предоставленных данных
    - Либо парсингом с hh.ru по ID
    """
    return await vacancy_service.create_vacancy(vacancy_data, hh_id)


@router.put("/update/{vacancy_id}", response_model=VacancySchema)
@router.patch("/update/{vacancy_id}", response_model=VacancySchema)
async def update_vacancy(
    vacancy_id: int,
    vacancy_data: VacancyUpdate,
    current_user: User = Depends(get_current_active_user),
    vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    """
    Обновление данных вакансии
    """
    return await vacancy_service.update_vacancy(vacancy_id, vacancy_data)


@router.get("/get/{vacancy_id}", response_model=VacancySchema)
async def get_vacancy(
    vacancy_id: int,
    current_user: User = Depends(get_current_active_user),
    vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    """
    Получение информации о вакнсии
    """
    return await vacancy_service.get_vacancy(vacancy_id)


@router.delete("/delete/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy(
    vacancy_id: int,
    current_user: User = Depends(get_current_active_user),
    vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    """
    Удаление вакансии
    """
    await vacancy_service.delete_vacancy(vacancy_id)
    return {"detail": "Вакансия успешно удалена"}


@router.post("/refresh-from-hh/{vacancy_id}", response_model=VacancySchema)
async def refresh_vacancy_from_hh(
    vacancy_id: int,
    current_user: User = Depends(get_current_active_user),
    vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    """
    Обновление данных вакансии из HH.ru по сохраненному hh_id
    """
    return await vacancy_service.refresh_vacancy_from_hh(vacancy_id)
