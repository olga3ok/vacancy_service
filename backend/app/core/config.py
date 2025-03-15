import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_NAME: str = os.getenv("POSTGRES_NAME", "vacancy_db")
    DB_ECHO_LOG: bool = os.getenv("DB_ECHO_LOG", "False").lower() == "true"

    HH_API_URL: str = os.getenv("HH_API_URL", "https://api.hh.ru/vacancies/")

    # Предустановленный пользователь
    DEFAULT_USERNAME: str = os.getenv("DEFAULT_USERNAME", "")
    DEFAULT_PASSWORD: str = os.getenv("DEFAULT_PASSWORD", "")

    @property
    def DATABASE_URL(self) -> str:
        """Формирование строки подключения к БД из отдельных параметров"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
