from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker
from datetime import datetime, timezone, timedelta
from sqlalchemy.future import select

from app.db.base import Database
from app.db.models import Vacancy
from app.utils.hh_parser import HHParser
from app.core.config import settings


broker = AioPikaBroker(
    settings.RABBITMQ_URL
)


scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


@broker.task(schedule=[{"cron": "0 */4 * * *"}])
async def update_all_vacancies_from_hh():
    """ Обновление информации обо всех вакансиях с HH.ru """
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

        return {"status": "success", "updated_at": datetime.now(timezone.utc).isoformat()}


@broker.task(schedule=[{"cron": "0 0 * * *"}])
async def mark_outdated_vacancies():
    """ Назначение статуса 'outdated' для вакансий, опубликованных на hh.ru более 2 недель назад """
    async for session in Database.get_db():
        stmt = select(Vacancy).where(Vacancy.hh_id.is_not(None))
        result = await session.execute(stmt)
        vacancies = result.scalars().all()

        two_weeks_ago = datetime.now(timezone.utc) - timedelta(weeks=2)
        updated_count = 0

        for vacancy in vacancies:
            if vacancy.published_at is None:
                    vacancy.published_at = datetime.now(timezone.utc)

            if vacancy.published_at < two_weeks_ago:
                vacancy.status = "outdated"
                updated_count += 1

        await session.commit()

    return {
        "status": "success",
        "updated_count": updated_count,
        "executed_at": datetime.now(timezone.utc).isoformat()
    }
