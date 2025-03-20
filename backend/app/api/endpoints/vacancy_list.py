from fastapi import Depends, APIRouter
from typing import List

from app.api.deps import get_current_active_user, get_vacancy_service
from app.core.utils.vacancy_service import VacancyService
from app.db.models import User
from app.schemas.vacancy import Vacancy as VacancySchema


router = APIRouter()


@router.get("/list", response_model=List[VacancySchema])
async def list_vacancies(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    vacancy_service: VacancyService = Depends(get_vacancy_service)
):
    """
    Получение списка вакансий
    """
    return await vacancy_service.get_vacancies_list(skip, limit)
