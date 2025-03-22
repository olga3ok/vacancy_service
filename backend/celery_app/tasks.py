import asyncio
import nest_asyncio
from celery_app.celery import celery_app
from datetime import datetime, timedelta, timezone
from sqlalchemy.future import select

from app.db.models import Vacancy
from app.db.base import Database
from app.services.hh_parser import HHParser


nest_asyncio.apply()


async def update_all_vacancies_from_hh_async():
    """
    Обвноление информации обо всех вакансиях с HH.ru
    """
    async for session in Database.get_db():
        stmt = select(Vacancy).where(Vacancy.hh_id.is_not(None))
        result = await session.execute(stmt)
        vacancies = result.scalars().all()

        for vacancy in vacancies:
            try:
                update_data = await HHParser.get_vacancy_from_hh(vacancy.hh_id)

                for key, value in update_data.dict().items():
                    if hasattr(vacancy, key):
                        setattr(vacancy, key, value)

                vacancy.updated_at = datetime.now(timezone.utc)

                await session.commit()
                await session.refresh(vacancy)

            except Exception as e:
                print(f"Error updating vacancy {vacancy.id}: {str(e)}")


@celery_app.task
def update_all_vacancies_from_hh_wrapper():
    asyncio.run(update_all_vacancies_from_hh_async())


async def mark_outdated_vacancies_async():
    """
    Назначение статуса 'outdated' для вакансий, опубликованных на hh.ru более 2 недель назад
    """
    async for session in Database.get_db():
        stmt = select(Vacancy).where(Vacancy.hh_id.is_not(None))
        result = await session.execute(stmt)
        vacancies = result.scalars().all()

        two_weeks_ago = datetime.now(timezone.utc) - timedelta(weeks=2)

        for vacancy in vacancies:
            if vacancy.published_at.tzinfo is None:
                vacancy.published_at = vacancy.published_at.replace(tzinfo=timezone.utc)

            if vacancy.published_at < two_weeks_ago:
                vacancy.status = 'outdated'
                await session.commit()


@celery_app.task
def mark_outdated_vacancies_wrapper():
    asyncio.run(mark_outdated_vacancies_async())
