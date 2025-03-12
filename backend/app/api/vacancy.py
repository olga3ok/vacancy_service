from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.db.models import Vacancy, User
from app.schemas.vacancy import VacancyCreate, Vacancy as VacancySchema, VacancyUpdate
from app.services.hh_parser import get_vacancy_from_hh
from app.api.auth import get_current_active_user


router = APIRouter()


@router.post("/create", response_model=VacancySchema)
async def create_vacancy(
    vacancy_data: VacancyCreate = None,
    hh_id: str = None,
    db: Session = Depends(get_db),
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
        existing_vacancy = db.query(Vacancy).filter(Vacancy.hh_id == vacancy_data.hh_id).first()
        if existing_vacancy:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vacancy with hh_id {vacancy_data.hh_id} already exists"
            )

    # Создание новой вакансии
    db_vacancy = Vacancy(**vacancy_data.dict())
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


@router.put("/update/{vacancy_id}", response_model=VacancySchema)
@router.patch("/update/{vacanct_id}", response_model=VacancySchema)
async def update_vacancy(
    vacancy_id: int,
    vacancy_data: VacancyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Обновление данных вакансии
    """
    # Поиск вакансии
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
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

    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


@router.get("/get/{vacancy_id}", response_model=VacancySchema)
async def get_vacancy(
    vacancy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Получение информации о вакнсии
    """
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail=f"Vacancy with id {vacancy_id} not found")
    return db_vacancy


@router.delete("/delete/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy(
    vacancy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Удаление вакансии
    """
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail=f"Vacancy with id {vacancy_id} not found")

    db.delete(db_vacancy)
    db.commit()
    return {"detail": "Vacancy deleted successfully"}


@router.get("/list", response_model=List[VacancySchema])
async def list_vacancies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Получение списка вакансий
    """
    vacancies = db.query(Vacancy).offset(skip).limit(limit).all()
    return vacancies
