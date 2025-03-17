from fastapi import APIRouter
from celery_app.tasks import update_all_vacancies_from_hh_wrapper, mark_outdated_vacancies_wrapper


router = APIRouter()


@router.post("/test-update-vacancies/")
async def test_update_vacancies():
    update_all_vacancies_from_hh_wrapper.apply_async()
    return {"message": "Task is running!"}


@router.post("/mark_outdated_vacancies/")
async def test_mar_outdated_vacancies():
    mark_outdated_vacancies_wrapper.apply_async()
    return {"message": "Task is running!"}
