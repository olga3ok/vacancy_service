from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy.future import select

from app.db.base import get_db
from app.db.models import Vacancy
from app.schemas.vacancy import Vacancy as VacancySchema


router = APIRouter()


@router.get("/list", response_model=List[VacancySchema])
async def list_vacancies(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Получение списка вакансий
    """
    stmt = select(Vacancy).offset(skip).limit(limit)
    result = await db.execute(stmt)
    vacancies = result.scalars().all()
    return vacancies