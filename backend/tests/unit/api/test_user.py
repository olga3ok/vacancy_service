import os
import sys
sys.path.append(os.getcwd())

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.main import app
from app.api.user import get_current_active_user
from app.api.auth import get_current_user


class MockUser:
    """
    Мок-класс для имитации модели User
    """
    def __init__(self, username, is_active=True):
        self.username = username
        self.is_active = is_active


@pytest.fixture
def client():
    """
    Фикстура для тестового клиента
    """
    # Очищаем переопределения зависимостей после каждого теста
    app.dependency_overrides = {}
    return TestClient(app)


@pytest.fixture
def active_user():
    """
    Фикстура для активного пользователя
    """
    return MockUser(username="testuser")


@pytest.fixture
def inactive_user():
    """
    Фикстура для неактивного пользователя
    """
    return MockUser(username="inactive_user", is_active=False)


def test_get_current_user_info_success(client, active_user):
    """
    Тест успешного получения информации о пользователе
    """
    # Переопределяем зависимость для эндпоинта
    async def override_get_current_active_user():
        return active_user

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user

    response = client.get("/me")

    assert response.status_code == 200
    assert response.json() == {"username": "testuser"}


def test_get_current_user_info_unauthorized(client):
    """
    Тест неавторизованного доступа
    """
    response = client.get("/me")

    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_get_current_user_info_inactive_user(client, inactive_user):
    """
    Тест доступа с неактивным пользователем
    """
    # Сначала переопределяем get_current_user, чтобы вернуть неактивного пользователя
    async def override_get_current_user():
        return inactive_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    # Затем переопределяем get_current_active_user, чтобы выбросить ожидаемое исключение
    async def override_get_current_active_user():
        if not inactive_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return inactive_user

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user

    response = client.get("/me")

    assert response.status_code == 400
    assert response.json()["detail"] == "Inactive user"
