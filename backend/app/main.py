import os
import sys

sys.path.append(os.getcwd())

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select

from app.api.endpoints import auth, vacancy, vacancy_list
from app.core.config import settings
from app.core.security import PasswordHelper
from app.db.base import Database
from app.db.models import User
from celery_app import celery_tests


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация при старте
    engine = Database.get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Database._base.metadata.create_all)

    # Дефолтный юзер
    await create_default_user()

    # Подключение к БД
    async for db in Database.get_db():
        try:
            yield
        finally:
            await db.close()


def create_app() -> FastAPI:
    app = FastAPI(title="Vacancy Service API", lifespan=lifespan)

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Регистрация роутеров
    app.include_router(auth.router, prefix="/auth", tags=["authentication"])
    app.include_router(vacancy.router, prefix="/api/v1/vacancy", tags=["vacancies"])
    app.include_router(vacancy_list.router, prefix="/api/v1/vacancies", tags=["vacancies-list"])
    app.include_router(celery_tests.router, tags=["celery_tests"])

    @app.get("/")
    async def root():
        return {"message": "Welcome to Vacancy Service API"}

    return app


async def create_default_user():
    async for db in Database.get_db():
        # Проверка существования пользователя с заданным именем
        stmt = select(User).where(User.username == settings.DEFAULT_USERNAME)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            # Создание пользователя, если он не существует
            pwd_helper = PasswordHelper()  # Создаем экземпляр класса
            new_user = User(
                username=settings.DEFAULT_USERNAME,
                hashed_password=pwd_helper.hash_password(settings.DEFAULT_PASSWORD),
                is_active=True
            )
            db.add(new_user)
            await db.commit()
            break
