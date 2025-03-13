import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    HH_API_URL: str = os.getenv("HH_API_URL", "https://api.hh.ru/vacancies/")

    # Предустановленный пользователь
    DEFAULT_USERNAME: str = os.getenv("DEFAULT_USERNAME", "")
    DEFAULT_PASSWORD: str = os.getenv("DEFAULT_PASSWORD", "")

settings = Settings()
