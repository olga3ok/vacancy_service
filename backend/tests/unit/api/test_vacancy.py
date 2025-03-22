import pytest
from fastapi import HTTPException

from app.main import app
from app.api.deps import get_current_active_user, get_vacancy_service


# Тест создания вакансии
@pytest.mark.asyncio
async def test_create_vacancy_success(client, mock_db, mock_user, mock_vacancy_service):
    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.post(
        "/api/v1/vacancy/create",
        json={
            "title": "Test Vacancy",
            "company_name": "Test Company",
            "company_address": "Test Address",
            "company_logo": "https://example.com/logo.png",
            "description": "Test Description",
            "status": "active",
        }
    )

    assert response.status_code == 200

    # Проверяем данные в ответе
    response_data = response.json()
    assert response_data["title"] == "Test Vacancy"
    assert response_data["company_name"] == "Test Company"
    assert response_data["status"] == "active"

    # Проверка, что сервис был вызван с правильными параметрами
    mock_vacancy_service.create_vacancy.assert_called_once()


# Тест создания вакансии с HH.ru по ID
@pytest.mark.asyncio
async def test_create_vacancy_from_hh_success(client, mock_user, mock_vacancy_service):
    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.post(
        "/api/v1/vacancy/create?hh_id=12345"
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Vacancy"
    assert response.json()["company_name"] == "Test Company"

    # Проверяем, что сервис был вызван с правильными параметрами
    mock_vacancy_service.create_vacancy.assert_called_once_with(None, "12345")


# Тест получения вакансии
@pytest.mark.asyncio
async def test_get_vacancy_success(client, mock_user, mock_vacancy_service):
    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.get(
    "/api/v1/vacancy/get/1",
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Test Vacancy"

    mock_vacancy_service.get_vacancy.assert_called_once_with(1)


# Тест обновления вакансии
@pytest.mark.asyncio
async def test_update_vacancy_success(client, mock_user, mock_vacancy_service):
    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.put(
        "/api/v1/vacancy/update/1",
        json={
            "title": "Updated Vacancy",
            "company_name": "Updated Company"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Vacancy"
    assert response.json()["company_name"] == "Test Company"

    # Проверяем, что сервис был вызван с правильными параметрами
    from app.schemas.vacancy import VacancyUpdate
    mock_vacancy_service.update_vacancy.assert_called_once()
    args, kwargs = mock_vacancy_service.update_vacancy.call_args
    assert args[0] == 1
    assert isinstance(args[1], VacancyUpdate)
    assert args[1].title == "Updated Vacancy"
    assert args[1].company_name == "Updated Company"


# Тест удаления вакансии
@pytest.mark.asyncio
async def test_delete_vacancy_success(client, mock_user, mock_vacancy_service):
    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.delete(
        "/api/v1/vacancy/delete/1"
    )

    assert response.status_code == 204

    # Проверяем, что сервис был вызван с правильными параметрами
    mock_vacancy_service.delete_vacancy.assert_called_once_with(1)


# Тест обновления вакансии с HH.ru
@pytest.mark.asyncio
async def test_refresh_vacancy_from_hh_success(client, mock_user, mock_vacancy_service):
    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.post(
        "/api/v1/vacancy/refresh-from-hh/1"
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Vacancy"
    assert response.json()["company_name"] == "Test Company"

    # Проверяем, что сервис был вызван с правильными параметрами
    mock_vacancy_service.refresh_vacancy_from_hh.assert_called_once_with(1)


# Тесты ошибок
# Тест - вакансия не найдена
@pytest.mark.asyncio
async def test_get_vacancy_not_found(client, mock_user, mock_vacancy_service):
    mock_vacancy_service.get_vacancy.side_effect = HTTPException(
        status_code=404,
        detail="Вакансия с ID 999 не найдена"
    )

    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.get(
        "/api/v1/vacancy/get/999",
    )

    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]

    # Проверяем, что сервис был вызван с правильными параметрами
    mock_vacancy_service.get_vacancy.assert_called_once_with(999)


# Тест - вакансия с таким hh_id уже существует
@pytest.mark.asyncio
async def test_create_vacancy_duplicate_hh_id(client, mock_user, mock_vacancy_service):
    from fastapi import HTTPException
    mock_vacancy_service.create_vacancy.side_effect = HTTPException(
        status_code=400,
        detail="Вакансия с ID 12345 с HH.ru уже существует"
    )

    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.post(
        "/api/v1/vacancy/create",
        json={
            "title": "Test Vacancy",
            "company_name": "Test Company",
            "company_address": "Test Address",
            "company_logo": "https://example.com/logo.png",
            "description": "Test Description",
            "status": "active",
            "hh_id": "12345"
        }
    )

    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


# Тест ошибки при обновлении с HH.ru
@pytest.mark.asyncio
async def test_refresh_vacancy_from_hh_error(client, mock_user, mock_vacancy_service):
    from fastapi import HTTPException
    mock_vacancy_service.refresh_vacancy_from_hh.side_effect = HTTPException(
        status_code=400,
        detail="Ошибка при получении вакансии с HH.ru"
    )

    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.post(
        "/api/v1/vacancy/refresh-from-hh/1"
    )

    assert response.status_code == 400
    assert "Ошибка при получении" in response.json()["detail"]


# Тест получения списка вакансий
@pytest.mark.asyncio
async def test_get_vacancies_list(client, mock_user, mock_vacancy_service, mock_vacancy):
    async def override_get_current_active_user():
        return mock_user

    async def override_get_vacancy_service():
        return mock_vacancy_service

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_vacancy_service] = override_get_vacancy_service

    response = client.get(
        "/api/v1/vacancies/list"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["title"] == "Test Vacancy"

    mock_vacancy_service.get_vacancies_list.assert_called_once_with(0, 100)
