from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.db.base import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String)
    title = Column(String)
    company_name = Column(String)
    company_address = Column(String)
    company_logo = Column(String) # URL to logo
    description = Column(Text)
    hh_id = Column(String, unique=True, index=True, nullable=True) # ID вакансии на hh.ru
