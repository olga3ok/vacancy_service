import os
import sys

sys.path.append(os.getcwd())

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timezone

from app.main import app
from app.db.base import get_db
from app.api.auth import get_current_active_user
from app.db.models import Vacancy
from app.schemas.vacancy import VacancyCreate, Vacancy as VacancySchema


@pytest.fixture
def client():
    """
    Фикстура для тестового клиента
    """
    # Очищаем переопределения зависимостей после каждого теста
    app.dependency_overrides = {}
    return TestClient(app)


@pytest.fixture
def mock_user():
    """
    Фикстура, которая создает мок-объект пользователя с предустановленными атрибутами
    """
    user = MagicMock()
    user.username = "testuser"
    user.hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 'password'
    user.is_active = True
    return user


# Фикстура для мок-объекта базы данных
@pytest.fixture
def mock_db():
    """
    Фикстура, которая создает асинхронный мок-объект для имитации базы данных
    """
    return AsyncMock()


@pytest.fixture
def mock_vacancy():
    """Мок объекта вакансии"""
    vacancy = MagicMock(spec=Vacancy)
    vacancy.id = 1
    vacancy.title = "Test Vacancy"
    vacancy.company_name = "Test Company"
    vacancy.company_address = "Test Address"
    vacancy.company_logo = "https://example.com/logo.png"
    vacancy.description = "Test Description"
    vacancy.status = "active"
    vacancy.hh_id = "12345"
    vacancy.published_at = datetime.now(timezone.utc)
    vacancy.created_at = datetime.now(timezone.utc)
    vacancy.updated_at = datetime.now(timezone.utc)
    return vacancy

# Тест создания вакансии
async def test_create_vacancy_success(client, mock_db, mock_user):
    mock_vacancy_for_create = VacancySchema(
        id=1,
        title="Test Vacancy",
        company_name="Test Company",
        company_address="Test Address",
        company_logo="https://example.com/logo.png",
        description="Test Description",
        status="active",
        created_at=datetime.now(),
        updated_at=None
    )

    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_vacancy_for_create  # Возвращаем мок-вакансию
    mock_db.execute.return_value = mock_result

    mock_db.refresh = AsyncMock()

    async def override_get_current_active_user():
        return mock_user

    async def override_get_db():
        return mock_db

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_db] = override_get_db

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


# Тест получения вакансии
def test_get_vacancy_success(client, mock_user, mock_db, mock_vacancy):
    # Настраиваем мок для БД
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_vacancy  # Возвращаем мок-вакансию
    mock_db.execute.return_value = mock_result

    async def override_get_current_active_user():
        return mock_user

    async def override_get_db():
        return mock_db

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_db] = override_get_db

    response = client.get(
    "/api/v1/vacancy/get/1",
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Test Vacancy"

# Тест обновления вакансии
def test_update_vacancy_success(client, mock_user, mock_db, mock_vacancy):
    # Настраиваем мок для БД
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_vacancy  # Возвращаем мок-вакансию
    mock_db.execute.return_value = mock_result

    # Настраиваем мок обновления
    mock_db.refresh = AsyncMock()

    async def override_get_current_active_user():
        return mock_user

    async def override_get_db():
        return mock_db

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_db] = override_get_db

    response = client.put(
        "/api/v1/vacancy/update/1",
        json={
            "title": "Updated Vacancy",
            "company_name": "Updated Company"
        }
    )

    assert response.status_code == 200
    assert "Updated Vacancy" in response.text
    assert "Updated Company" in response.text


# Тест удаления вакансии
def test_delete_vacancy_success(client, mock_user, mock_db, mock_vacancy):
    # Настраиваем мок для БД
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_vacancy  # Возвращаем мок-вакансию
    mock_db.execute.return_value = mock_result

    async def override_get_current_active_user():
        return mock_user

    async def override_get_db():
        return mock_db

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_db] = override_get_db
    # Патчим зависимости

    response = client.delete(
        "/api/v1/vacancy/delete/1"
    )

    assert response.status_code == 204


# Тест обновления вакансии с HH.ru
def test_refresh_vacancy_from_hh_success(client, mock_user, mock_db, mock_vacancy):
    # Настраиваем мок для БД
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_vacancy
    mock_db.execute.return_value = mock_result

    # Настраиваем мок обновления
    mock_db.refresh = AsyncMock()

    async def override_get_current_active_user():
        return mock_user

    async def override_get_db():
        return mock_db

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_db] = override_get_db
    # Мок для функции парсинга с HH.ru
    mock_hh_data = VacancyCreate(
        title="HH Vacancy",
        company_name="HH Company",
        company_address="HH Address",
        company_logo="https://hh.ru/logo.png",
        description="HH Description",
        status="active",
        hh_id="12345"
    )

    # Патчим зависимости
    with patch('app.api.vacancy.get_vacancy_from_hh', AsyncMock(return_value=mock_hh_data)):

        response = client.post(
            "/api/v1/vacancy/refresh-from-hh/1"
        )

        assert response.status_code == 200
        assert "HH Vacancy" in response.text
        assert "HH Company" in response.text


# Тест создания вакансии с HH.ru по ID
@pytest.mark.skip
def test_create_vacancy_from_hh_success(client, mock_user, mock_db, mock_vacancy):
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_vacancy
    mock_db.execute.return_value = mock_result

    # Настраиваем мок обновления
    mock_db.refresh = AsyncMock()

    async def override_get_current_active_user():
        return mock_user

    async def override_get_db():
        return mock_db

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_db] = override_get_db
    # Мок для функции парсинга с HH.ru
    mock_hh_data = VacancySchema(

        title="Test Vacancy",
        company_name="Test Company",
        company_address="Test Address",
        company_logo="https://example.com/logo.png",
        description="Test Description",
        status="active",
        created_at=datetime.now(),
    )
    # Патчим зависимости
    with patch('app.api.vacancy.get_vacancy_from_hh', AsyncMock(return_value=mock_hh_data)):
        response = client.post(
            "/api/v1/vacancy/create",
            json={
                "hh_id": "12345"
            }
        )

        assert response.status_code == 200
        assert "HH Vacancy" in response.text
        assert "HH Company" in response.text

# Тесты ошибок

# Тест - вакансия не найдена
def test_get_vacancy_not_found(client, mock_user, mock_db):
    # Настраиваем мок для БД - вакансия не найдена
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = None
    mock_db.execute.return_value = mock_result

    async def override_get_current_active_user():
        return mock_user

    async def override_get_db():
        return mock_db

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_db] = override_get_db

    response = client.get(
    "/api/v1/vacancy/get/999",
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


# Тест - вакансия с таким hh_id уже существует
def test_create_vacancy_duplicate_hh_id(client, mock_user, mock_db, mock_vacancy):
    # Настраиваем мок для БД - вакансия с таким hh_id уже существует
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_vacancy
    mock_db.execute.return_value = mock_result

    async def override_get_current_active_user():
        return mock_user

    async def override_get_db():
        return mock_db

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_db] = override_get_db

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
    assert "already exists" in response.json()["detail"]


# Тест ошибки при обновлении с HH.ru
def test_refresh_vacancy_from_hh_error(client, mock_user, mock_db, mock_vacancy):
    # Настраиваем мок для БД
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_vacancy
    mock_db.execute.return_value = mock_result

    async def override_get_current_active_user():
        return mock_user

    async def override_get_db():
        return mock_db

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    app.dependency_overrides[get_db] = override_get_db
    # Патчим зависимости, вызывая ошибку при парсинге HH
    with patch('app.api.vacancy.get_vacancy_from_hh', AsyncMock(side_effect=Exception("HH API error"))):

        response = client.post(
            "/api/v1/vacancy/refresh-from-hh/1"
        )

        assert response.status_code == 400
        assert "Error fetching" in response.json()["detail"]
