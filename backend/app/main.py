import os
import sys

sys.path.append(os.getcwd())

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import auth, vacancy, vacancy_list
from app.core.config import settings
from app.core.security import PasswordHelper
from app.db.base import Database
from app.repositories.user_repository import UserRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация при старте
    engine = Database.get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Database._base.metadata.create_all)

    # Дефолтный юзер
    await create_default_user()

    # Подключение к БД
    async with Database.get_engine().connect() as connection:
        yield


async def create_default_user():
    async for db in Database.get_db():
        user_repo = UserRepository(db)
        user = await user_repo.get_by_username(settings.DEFAULT_USERNAME)

        if not user:
            # Создание пользователя, если он не существует
            pwd_helper = PasswordHelper()
            user_data = {
                "username": settings.DEFAULT_USERNAME,
                "hashed_password": pwd_helper.hash_password(settings.DEFAULT_PASSWORD),
                "is_active": True
            }
            await user_repo.create(user_data)

        await db.commit()
        break



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

    @app.get("/")
    async def root():
        return {"message": "Welcome to Vacancy Service API"}

    return app


app = create_app()
