import psycopg2 
from argon2 import PasswordHasher

# Инициализация хэшера Argon2
ph = PasswordHasher()

def get_connection():
    """Создает и возвращает подключение к базе данных PostgreSQL"""
    try:
        conn = psycopg2.connect(
            dbname='curs',
            user='postgres',
            password='123',
            host='localhost',
            port=5432
        )
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def init_db():
    """Инициализация базы данных и создание таблиц"""
    conn = get_connection()
    if not conn:
        print("Не удалось подключиться к базе данных")
        return None
    
    cursor = conn.cursor()
                # Создаем администратора по умолчанию, если его нет
    try:
        admin_hash = ph.hash("admin123")
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
            ("admin", admin_hash, "admin")
        )
    except psycopg2.IntegrityError:
        conn.rollback()  # Админ уже существует
    else:
        conn.commit()
        
    conn.commit()
    print("База данных инициализирована успешно!")
    return conn
    