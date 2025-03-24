import os
import sys
sys.path.append(os.getcwd())

import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from app.schemas.vacancy import Vacancy
from app.schemas.user import UserResponse
from app.schemas.token import Token
from app.services.vacancy_service import VacancyService
from app.services.auth_service import AuthService
from app.main import app


@pytest.fixture
def client():
    """ Фикстура для тестового клиента """
    # Очищаем переопределения зависимостей после каждого теста
    app.dependency_overrides = {}
    return TestClient(app)


@pytest.fixture
def mock_user():
    """ Фикстура, которая создает мок-объект пользователя с предустановленными атрибутами  """
    user = MagicMock()
    user.username = "testuser"
    user.hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # 'password'
    user.is_active = True
    return user


@pytest.fixture
def mock_db():
    """ Фикстура, которая создает асинхронный мок-объект для имитации базы данных """
    return AsyncMock()


@pytest.fixture
def mock_vacancy():
    """ Мок объекта вакансии """
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


@pytest.fixture
def mock_vacancy_service(mock_db, mock_vacancy):
    """ Фикстура для создания мок-сервиса вакансий """
    service = AsyncMock(spec=VacancyService)
    service.get_vacancy.return_value = mock_vacancy
    service.create_vacancy.return_value = mock_vacancy
    service.update_vacancy.return_value = mock_vacancy
    service.delete_vacancy.return_value = None
    service.refresh_vacancy_from_hh.return_value = mock_vacancy
    service.get_vacancies_list.return_value = [mock_vacancy]
    return service


@pytest.fixture
def mock_auth_service(mock_db, mock_user):
    """ Фикстура для создания мок-сервиса аутентификации """
    service = AsyncMock(spec=AuthService)
    service.register_user.return_value = UserResponse(id=mock_user.id, username=mock_user.username, is_active=mock_user.is_active)
    service.login_user.return_value = Token(access_token="mock_access_token", token_type="bearer")
    service.logout_user.return_value = UserResponse(id=mock_user.id, username=mock_user.username, is_active=False)
    service.refresh_token.return_value = {"access_token": "new_mock_access_token", "token_type": "bearer"}
    service.get_current_user_with_token.return_value = mock_user
    return service
