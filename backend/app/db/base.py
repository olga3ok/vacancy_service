from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings
from app.db.unit_of_work import UnitOfWorkFactory


class Database:
    _engine = None
    _session_local = None
    _base = declarative_base()

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls._engine = create_async_engine(
                settings.DATABASE_URL,
                echo=settings.DB_ECHO_LOG
            )
        return cls._engine

    @classmethod
    def get_session_local(cls):
        if cls._session_local is None:
            cls._session_local = sessionmaker(
                autocommit=False,
                autoflush=False,
                class_=AsyncSession,
                expire_on_commit=False,
                bind=cls.get_engine()
            )
        return cls._session_local

    @classmethod
    async def get_db(cls):
        session_local = cls.get_session_local()
        async with session_local() as session:
            try:
                yield session
            finally:
                await session.close()

    @classmethod
    def get_unit_of_work_factory(cls):
        """ Создание фабрики Unit of Work """
        session_local = cls.get_session_local()
        return UnitOfWorkFactory(session_local)
