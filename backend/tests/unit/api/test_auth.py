import pytest
from fastapi import HTTPException

from app.main import app
from app.api.deps import get_auth_service, get_current_active_user


# Тест успешной регистрации пользователя
@pytest.mark.asyncio
async def test_register_user_success(client, mock_auth_service):
    async def override_get_auth_service():
        return mock_auth_service

    app.dependency_overrides[get_auth_service] = override_get_auth_service

    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "password": "password"
        }
    )

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["username"] == "testuser"
    assert response_data["is_active"] is True

    mock_auth_service.register_user.asser_called_once()


# Тест успешной аутентификации пользователя
@pytest.mark.asyncio
async def test_login_user_success(client, mock_auth_service):
    async def override_get_auth_service():
        return mock_auth_service

    app.dependency_overrides[get_auth_service] = override_get_auth_service

    response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "password"
        }
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["access_token"] == "mock_access_token"
    assert response_data["token_type"] == "bearer"

    mock_auth_service.login_user.assert_called_once()


# Тест успешного выхода пользователя
@pytest.mark.asyncio
async def test_logout_user_success(client, mock_auth_service):
    async def override_get_auth_service():
        return mock_auth_service

    app.dependency_overrides[get_auth_service] = override_get_auth_service

    response = client.post(
        "/auth/logout",
        headers={"Authorization": "Bearer mock_access_token"}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == "testuser"
    assert response_data["is_active"] is False

    mock_auth_service.logout_user.assert_called_once()


# Тест успешного обновления токена
@pytest.mark.asyncio
async def test_refresh_token_success(client, mock_auth_service):
    async def override_get_auth_service():
        return mock_auth_service

    app.dependency_overrides[get_auth_service] = override_get_auth_service

    response = client.post(
        "/auth/refresh?refresh_token=mock_refresh_token"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["access_token"] == "new_mock_access_token"
    assert response_data["token_type"] == "bearer"

    mock_auth_service.refresh_token.assert_called_once()


# Тест получения информации о текущем пользователе
@pytest.mark.asyncio
async def test_read_users_me_success(client, mock_auth_service, mock_user):
    async def override_get_current_active_user():
        return mock_user

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user

    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer mock_access_token"}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == "testuser"
    assert response_data["is_active"] is True


# Тесты ошибок
# Тест регистрации пользователя, который уже существует
@pytest.mark.asyncio
async def test_register_user_exists(client, mock_auth_service):
    mock_auth_service.register_user.side_effect = HTTPException(
        status_code=400,
        detail="User already exists"
    )

    async def override_get_auth_service():
        return mock_auth_service

    app.dependency_overrides[get_auth_service] = override_get_auth_service

    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "password": "password"
        }
    )

    assert response.status_code == 400
    assert "User already exists" in response.json()["detail"]


# Тест аутентификации с неверными учетными данными
@pytest.mark.asyncio
async def test_login_user_invalid_credentials(client, mock_auth_service):
    mock_auth_service.login_user.side_effect = HTTPException(
        status_code=401,
        detail="Incorrect username or password"
    )

    async def override_get_auth_service():
        return mock_auth_service

    app.dependency_overrides[get_auth_service] = override_get_auth_service

    response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


# Тест обновления токена с неверным токеном обновления
@pytest.mark.asyncio
async def test_refresh_token_invalid(client, mock_auth_service):
    mock_auth_service.refresh_token.side_effect = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    async def override_get_auth_service():
        return mock_auth_service

    app.dependency_overrides[get_auth_service] = override_get_auth_service

    response = client.post(
        "/auth/refresh?refresh_token=invalid_refresh_token"
    )

    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]
