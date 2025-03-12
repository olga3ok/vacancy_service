from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VacancyBase(BaseModel):
    title: str
    company_name: str
    company_address: str
    company_logo: str
    description: str
    status: str
    hh_id: Optional[str] = None


class VacancyCreate(VacancyBase):
    pass


class VacancyUpdate(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    company_logo: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    hh_id: Optional[str] = None


class VacancyInDB(VacancyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Vacancy(VacancyInDB):
    pass
