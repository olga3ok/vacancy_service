import os
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()


@dataclass(frozen=True)
class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 300

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "vacancy_db")
    DB_ECHO_LOG: bool = os.getenv("DB_ECHO_LOG", "False").lower() == "true"

    HH_API_URL: str = os.getenv("HH_API_URL", "https://api.hh.ru/vacancies/")

    # Предустановленный пользователь
    DEFAULT_USERNAME: str = os.getenv("DEFAULT_USERNAME", "")
    DEFAULT_PASSWORD: str = os.getenv("DEFAULT_PASSWORD", "")


    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "")

    @property
    def DATABASE_URL(self) -> str:
        """Формирование строки подключения к БД из отдельных параметров"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
