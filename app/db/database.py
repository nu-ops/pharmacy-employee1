from sqlmodel import SQLModel, create_engine, Session
from argon2 import PasswordHasher
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

# Инициализация хэшера Argon2
ph = PasswordHasher()

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost:5432/curs")

# Создание движка
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    """Возвращает новую сессию базы данных"""
    return Session(engine)

def init_db():
    """
    Инициализация базы данных:
    Убеждается, что таблицы существуют (без изменения структуры)
    """
    SQLModel.metadata.create_all(engine)

    print("База данных готова к работе")
    return engine