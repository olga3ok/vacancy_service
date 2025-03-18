import os
import sys
sys.path.append(os.getcwd())

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from jose import jwt
from fastapi import HTTPException

from app.main import app
from app.api.auth import get_user, get_current_user, get_current_active_user
from app.core.config import settings


# Создаем фикстуру для клиента
@pytest.fixture
def client():
    """
    Фикстура, которая создает тестовый клиент FastAPI для выполнения HTTP-запросов
    """
    return TestClient(app)


# Фикстура для мок-объекта базы данных
@pytest.fixture
def mock_db():
    """
    Фикстура, которая создает асинхронный мок-объект для имитации базы данных
    """
    return AsyncMock()


# Фикстура для мок-объекта пользователя
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


# Тесты для функции get_user
@pytest.mark.asyncio
async def test_get_user_existing(mock_db, mock_user):
    """
    Тест проверяет, что функция get_user правильно находит существующего пользователя в базе данных
    """
    # Настройка mock_db для возврата пользователя
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_user
    mock_db.execute.return_value = mock_result

    user = await get_user(mock_db, "testuser")

    assert user == mock_user
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_nonexistent(mock_db):
    """
    Тест проверяет, что функция get_user возвращает None, если пользователь не найден
    """
    # Настройка mock_db для возврата None
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = None
    mock_db.execute.return_value = mock_result

    user = await get_user(mock_db, "nonexistentuser")

    assert user is None
    mock_db.execute.assert_called_once()


# Тесты для функции get_current_user
@pytest.mark.asyncio
async def test_get_current_user_valid_token(mock_db, mock_user):
    """
    Тест проверяет, что функция get_current_user правильно обрабатывает действительный JWT-токен
    и возвращает соответствующего пользователя
    """
    # Создаем валидный токен
    test_token = "valid_token"

    # Используем патч для jwt.decode, чтобы избежать реальной проверки токена
    with patch('app.api.auth.jwt.decode') as mock_jwt_decode, \
         patch('app.api.auth.get_user', return_value=mock_user) as mock_get_user:

        # Настраиваем мок для jwt.decode, чтобы вернуть валидные данные
        mock_jwt_decode.return_value = {"sub": "testuser"}

        user = await get_current_user(test_token, mock_db)

        assert user == mock_user
        mock_jwt_decode.assert_called_once_with(test_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        mock_get_user.assert_called_once_with(mock_db, username="testuser")


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mock_db):
    """
    Тест проверяет, что функция get_current_user выбрасывает исключение HTTPException
    при получении недействительного JWT-токена
    """
    # Создаем недействительный токен
    access_token = "invalid.token.here"

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(access_token, mock_db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"


@pytest.mark.asyncio
async def test_get_current_user_missing_username(mock_db):
    """
    Тест проверяет, что функция get_current_user выбрасывает исключение HTTPException,
    если в токене отсутствует поле 'sub' (имя пользователя)
    """
    # Создаем токен без 'sub' поля
    access_token = jwt.encode(
        {"not_sub": "testuser"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(access_token, mock_db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"


@pytest.mark.asyncio
async def test_get_current_user_nonexistent_user(mock_db):
    """
    Тест проверяет, что функция get_current_user выбрасывает исключение HTTPException,
    если пользователь с указанным в токене именем не существует в базе данных
    """
    # Создаем действительный токен
    access_token = jwt.encode(
        {"sub": "testuser"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    # Настраиваем мок для возврата None
    with patch('app.api.auth.get_user', return_value=None) as mock_get_user:
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(access_token, mock_db)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Could not validate credentials"
        mock_get_user.assert_called_once_with(mock_db, username="testuser")


# Тест для функции get_current_active_user
@pytest.mark.asyncio
async def test_get_current_active_user_active(mock_user):
    """
    Тест проверяет, что функция get_current_active_user успешно возвращает пользователя,
    если его статус активен (is_active=True)
    """
    mock_user.is_active = True

    user = await get_current_active_user(mock_user)

    assert user == mock_user


@pytest.mark.asyncio
async def test_get_current_active_user_inactive(mock_user):
    """
    Тест проверяет, что функция get_current_active_user выбрасывает исключение HTTPException,
    если статус пользователя неактивен (is_active=False)
    """
    mock_user.is_active = False

    with pytest.raises(HTTPException) as exc_info:
        await get_current_active_user(mock_user)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Inactive user"


# Тесты для эндпоинта /token
@pytest.mark.asyncio
async def test_login_for_access_token_valid(client, mock_db, mock_user):
    """
    Тест проверяет успешную аутентификацию пользователя при отправке правильных учетных данных.
    Эндпоинт должен вернуть JSON с JWT-токеном и типом токена
    """
    # Настраиваем патчи для функций
    with patch('app.api.auth.get_user', return_value=mock_user), \
         patch('app.api.auth.verify_password', return_value=True), \
         patch('app.api.auth.create_access_token', return_value="mocked_token"):

        response = client.post(
            "/token",
            data={"username": "testuser", "password": "password"}
        )

        assert response.status_code == 200
        assert response.json() == {"access_token": "mocked_token", "token_type": "bearer"}


@pytest.mark.asyncio
async def test_login_for_access_token_invalid_username(client, mock_db):
    """
    Тест проверяет, что эндпоинт возвращает ошибку 401,
    если пользователь с указанным именем не существует в базе данных
    """
    # Настраиваем патчи для функций
    with patch('app.api.auth.get_user', return_value=None):

        response = client.post(
            "/token",
            data={"username": "wronguser", "password": "password"}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_login_for_access_token_invalid_password(client, mock_db, mock_user):
    """
    Тест проверяет, что эндпоинт возвращает ошибку 401,
    если пароль не соответствует хешированному паролю в базе данных
    """
    # Настраиваем патчи для функций
    with patch('app.api.auth.get_user', return_value=mock_user), \
         patch('app.api.auth.verify_password', return_value=False):

        response = client.post(
            "/token",
            data={"username": "testuser", "password": "wrongpassword"}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"
