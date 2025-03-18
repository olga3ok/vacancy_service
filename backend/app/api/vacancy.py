from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.auth import get_current_active_user
from app.db.base import get_db
from app.db.models import Vacancy, User
from app.schemas.vacancy import VacancyCreate, Vacancy as VacancySchema, VacancyUpdate
from app.services.hh_parser import get_vacancy_from_hh


router = APIRouter()


@router.post("/create", response_model=VacancySchema)
async def create_vacancy(
    vacancy_data: VacancyCreate = None,
    hh_id: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Создание вакансии:
    - Либо из предоставленных данных
    - Либо парсингом с hh.ru по ID
    """
    if hh_id:
        try:
            # Получение данных с hh.ru
            vacancy_data = await get_vacancy_from_hh(hh_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error fetching vacancy from HH.ru: {str(e)}"
            )

    if not vacancy_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either vacancy data or hh_id must be provided"
        )

    # Проверка существования вакансии с таким hh_id
    if vacancy_data.hh_id:
        stmt = select(Vacancy).where(Vacancy.hh_id == vacancy_data.hh_id)
        result = await db.execute(stmt)
        existing_vacancy = result.scalars().first()

        if existing_vacancy:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vacancy with hh_id {vacancy_data.hh_id} already exists"
            )

    # Создание новой вакансии
    db_vacancy = Vacancy(**vacancy_data.dict())
    db.add(db_vacancy)
    await db.commit()
    await db.refresh(db_vacancy)

    print(db_vacancy)
    return db_vacancy


@router.put("/update/{vacancy_id}", response_model=VacancySchema)
@router.patch("/update/{vacancy_id}", response_model=VacancySchema)
async def update_vacancy(
    vacancy_id: int,
    vacancy_data: VacancyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Обновление данных вакансии
    """
    # Поиск вакансии
    stmt = select(Vacancy).where(Vacancy.id == vacancy_id)
    result = await db.execute(stmt)
    db_vacancy = result.scalars().first()

    if db_vacancy is None:
        raise HTTPException(status_code=404, detail=f"Vacancy with id {vacancy_id} not found")

    # Если передан hh_id, то обновляем данные с hh.ru
    if vacancy_data.hh_id and vacancy_data.hh_id != db_vacancy.hh_id:
        try:
            updated_data = await get_vacancy_from_hh(vacancy_data.hh_id)
            vacancy_data_dict = vacancy_data.dict(exclude_unset=True)
            for key, value in updated_data.dict().items():
                if key not in vacancy_data_dict or vacancy_data_dict[key] is None:
                    vacancy_data_dict[key] = value

            # Обновляем объект вакансии
            for key, value in vacancy_data_dict.items():
                if hasattr(db_vacancy, key) and value is not None:
                    setattr(db_vacancy, key, value)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error fetching vacancy from HH.ru: {str(e)}"
            )
    else:
        # Обновляем только предоставленные поля
        for key, value in vacancy_data.dict(exclude_unset=True).items():
            if hasattr(db_vacancy, key) and value is not None:
                setattr(db_vacancy, key, value)

    db_vacancy.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(db_vacancy)
    return db_vacancy


@router.get("/get/{vacancy_id}", response_model=VacancySchema)
async def get_vacancy(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Получение информации о вакнсии
    """
    stmt = select(Vacancy).where(Vacancy.id == vacancy_id)
    result = await db.execute(stmt)
    db_vacancy = result.scalars().first()

    if db_vacancy is None:
        raise HTTPException(status_code=404, detail=f"Vacancy with id {vacancy_id} not found")
    return db_vacancy


@router.delete("/delete/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Удаление вакансии
    """
    stmt = select(Vacancy).where(Vacancy.id == vacancy_id)
    result = await db.execute(stmt)
    db_vacancy = result.scalars().first()

    if db_vacancy is None:
        raise HTTPException(status_code=404, detail=f"Vacancy with id {vacancy_id} not found")

    await db.delete(db_vacancy)
    await db.commit()
    return {"detail": "Vacancy deleted successfully"}


@router.post("/refresh-from-hh/{vacancy_id}", response_model=VacancySchema)
async def refresh_vacancy_from_hh(
    vacancy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Обновление данных вакансии из HH.ru по сохраненному hh_id
    """
    # Поиск вакансии во внутренней БД
    stmt = select(Vacancy).where(Vacancy.id == vacancy_id)
    result = await db.execute(stmt)
    db_vacancy = result.scalars().first()

    if db_vacancy is None:
        raise HTTPException(status_code=404, detail=f"Vacancy with id {vacancy_id} not found")

    # Проверка наличия hh_id
    if not db_vacancy.hh_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This vacancy doesn't have an associated HH.ru ID"
        )

    try:
        # Получение обновленных данных с hh.ry
        updated_data = await get_vacancy_from_hh(db_vacancy.hh_id)

        for key, value in updated_data.dict().items():
            if hasattr(db_vacancy, key):
                setattr(db_vacancy, key, value)

        db_vacancy.updated_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(db_vacancy)
        return db_vacancy

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching vanancy from HH.ru: {str(e)}"
        )
