import os
import sys
sys.path.append(os.getcwd())

from passlib.context import CryptContext
from app.db.models import User
from app.db.base import SessionLocal


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add_user(username: str, password: str):
    db = SessionLocal()
    hashed_password = pwd_context.hash(password)

    # Проверка существования пользователя
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        print(f"Пользователь '{username}' уже существует")
        return

    # Добавление нового пользователя
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.close()
    print(f"Пользователь '{username}' успешно добавлен.")


if __name__ == "__main__":
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    add_user(username, password)
