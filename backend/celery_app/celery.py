from celery import Celery
from celery.schedules import crontab
from app.core.config import settings


celery_app = Celery(
    'tasks',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['celery_app.tasks']
)

celery_app.conf.update(
    result_expires=3600,
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    beat_schedule={
        'update-vacancies-every-4-hours': {
            'task': 'celery_app.tasks.update_all_vacancies_from_hh_wrapper',
            'schedule': crontab(minute=0, hour='*/4'),
        },
        'mark-outdated-vacancies-daily': {
            'task': 'celery_app.tasks.mark_outdated_vacancies_wrapper',
            'schedule': crontab(minute=0, hour=0),
        },
    }
)

if __name__ == '__main__':
    celery_app.start()
