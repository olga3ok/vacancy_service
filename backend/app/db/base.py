from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


# Создание асинхронного движка
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO_LOG
)

#Создание асинхронной сессии
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
    bind=async_engine
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
