import asyncio
import os
import sys
sys.path.append(os.getcwd())

from app.db.base import Database
from app.schemas.user import UserCreate
from app.core.utils.auth_service import AuthService
from app.repositories.user_repository import UserRepository



async def add_user(username: str, password: str):
    """
    Асинхронное добавление нового пользователя в базу
    """
    async for db in Database.get_db():
        user_repo = UserRepository(db)
        auth_service = AuthService(session=db, user_repo=user_repo)

        existing_user = await user_repo.get_by_username(username)
        if existing_user:
            print(f"Пользователь '{username}' уже существует")
            return

        try:
            # Добавление нового пользователя
            user_data = UserCreate(username=username, password=password)
            user = await auth_service.register_user(user_data)

            if not user.is_active:
                await user_repo.update(user.id, {"is_active": True})
                await db.commit()

            print(f"Пользователь '{username}' успешно добавлен.")
        except Exception as e:
            print(f"Ошибка при создании пользователя: {str(e)}")


async def main():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    await add_user(username, password)


if __name__ == "__main__":
    asyncio.run(main())
