import pytest
from fastapi import HTTPException

from app.main import app
from app.api.deps import get_current_active_user, get_vacancy_service


# Тест успешного получения списка вакансий
@pytest.mark.asyncio
async def test_list_vacancies_success(client, mock_user, mock_vacancy_service):
    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.get("/api/v1/vacancies/list")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["title"] == "Test Vacancy"

    mock_vacancy_service.get_vacancies_list.assert_called_once_with(0, 100)


# Тест получения пустого списка вакансий
@pytest.mark.asyncio
async def test_list_vacancies_empty(client, mock_user, mock_vacancy_service):
    mock_vacancy_service.get_vacancies_list.return_value = []

    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.get("/api/v1/vacancies/list")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 0

    mock_vacancy_service.get_vacancies_list.assert_called_once_with(0, 100)


# Тесты ошибок
# Ошибка сервиса
@pytest.mark.asyncio
async def test_list_vacancies_service_error(client, mock_user, mock_vacancy_service):
    mock_vacancy_service.get_vacancies_list.side_effect = HTTPException(
        status_code=500,
        detail="Internal Server Error"
    )

    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.get("/api/v1/vacancies/list")

    assert response.status_code == 500
    assert "Internal Server Error" in response.json()["detail"]

    mock_vacancy_service.get_vacancies_list.assert_called_once_with(0, 100)
