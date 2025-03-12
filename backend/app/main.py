import os
import sys
sys.path.append(os.getcwd())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, vacancy
from app.db.base import engine, Base, get_db
from app.db.models import User
from app.core.config import settings
from app.core.security import get_password_hash


app = FastAPI(title="Vacancy Service API")


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Создание таблиц в БД
Base.metadata.create_all(bind=engine)


# Регистрация роутеров
app.include_router(auth.router, tags=["authentification"])
app.include_router(vacancy.router, prefix="/api/v1/vacancy", tags=["vacancies"])


@app.on_event("startup")
async def create_default_user():
    db = next(get_db())
    # Проверка сущестования пользователя с заданным именем
    user = db.query(User).filter(User.username == settings.DEFAULT_USERNAME).first()
    if not user:
        # Создание пользователя, если он не существует
        new_user = User(
            username=settings.DEFAULT_USERNAME,
            hashed_password=get_password_hash(settings.DEFAULT_PASSWORD),
            is_active=True
        )
        db.add(new_user)
        db.commit()


@app.get("/")
async def root():
    return {"message": "Welcome to Vacancy Service API"}
