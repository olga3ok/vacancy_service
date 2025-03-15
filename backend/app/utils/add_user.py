import os
import sys
import asyncio
sys.path.append(os.getcwd())

from passlib.context import CryptContext
from sqlalchemy import select
from app.db.models import User
from app.db.base import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def add_user(username: str, password: str):
    """
    Асинхронное добавление нового пользователя в базу
    """
    async for db in get_db():
        hashed_password = pwd_context.hash(password)

        # Проверка существования пользователя
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        existing_user = result.scalars().first()

        if existing_user:
            print(f"Пользователь '{username}' уже существует")
            return

        # Добавление нового пользователя
        new_user = User(username=username, hashed_password=hashed_password)
        db.add(new_user)
        await db.commit()
        print(f"Пользователь '{username}' успешно добавлен.")


async def main():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    await add_user(username, password)


if __name__ == "__main__":
    asyncio.run(main())
