from fastapi import HTTPException, status


class AuthException(HTTPException):
    """ Базовый класс для ошибок аутентификации """
    def __init__ (self, detail: str):
        """ Инициализация с указанием детальной информации об ошибке """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class InactiveUserException(HTTPException):
    """ Исключение для неактивного пользователя """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )


class InvalidCredentialsException(AuthException):
    """ Исключение для неверных учетных данных """
    def __init__(self):
        super().__init__(detail="Incorrect username or password")


class TokenValidationException(AuthException):
    """ Исключение для ошибок валидации токена """
    def __init__(self):
        super().__init__(detail="Could not validate credentials")


class UserExistsException(HTTPException):
    """ Исключение для случая, когда пользователь уже существует """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
