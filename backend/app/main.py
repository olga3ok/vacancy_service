import os
import sys
sys.path.append(os.getcwd())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, vacancy, user, vacancy_list
from app.db.base import async_engine, Base, get_db
from app.db.models import User
from app.core.config import settings
from app.core.security import get_password_hash
from sqlalchemy.future import select


app = FastAPI(title="Vacancy Service API")


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Регистрация роутеров
app.include_router(auth.router, tags=["authentification"])
app.include_router(vacancy.router, prefix="/api/v1/vacancy", tags=["vacancies"])
app.include_router(vacancy_list.router, prefix="/api/v1/vacancies", tags=["vacancies-list"])
app.include_router(user.router, tags=["user"])


@app.on_event("startup")
async def setup():
    # Создание таблиц в БД
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_default_user():
    async for db in get_db():
        # Проверка сущестования пользователя с заданным именем
        stmt = select(User).where(User.username == settings.DEFAULT_USERNAME)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
        # Создание пользователя, если он не существует
            new_user = User(
                username=settings.DEFAULT_USERNAME,
                hashed_password=get_password_hash(settings.DEFAULT_PASSWORD),
                is_active=True
            )
            db.add(new_user)
            await db.commit()


@app.get("/")
async def root():
    return {"message": "Welcome to Vacancy Service API"}
