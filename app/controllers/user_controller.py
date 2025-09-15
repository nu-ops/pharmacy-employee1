from db.database import get_connection, ph
from argon2.exceptions import VerifyMismatchError
import psycopg2

def register_user(username, password, role="user"):
    """
    Регистрирует нового пользователя
    :param username: Имя пользователя
    :param password: Пароль
    :param role: Роль пользователя (user/admin)
    :return: True если успешно, False если пользователь уже существует
    """
    conn = get_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    try:
        password_hash = ph.hash(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
            (username, password_hash, role)
        )
        conn.commit()
        print(f"Пользователь '{username}' успешно зарегистрирован")
        return True
    except psycopg2.IntegrityError:
        conn.rollback()
        print("Пользователь с таким именем уже существует")
        return False
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при регистрации: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def authorize_user(username, password):
    """
    Авторизует пользователя
    :param username: Имя пользователя
    :param password: Пароль
    :return: Данные пользователя если успешно, None если нет
    """
    conn = get_connection()
    if not conn:
        return None
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username = %s",
            (username,)
        )
        row = cursor.fetchone()
        
        if row is None:
            print("Пользователь не найден")
            return None
        
        # Преобразуем в словарь
        columns = [desc[0] for desc in cursor.description]
        user = dict(zip(columns, row))
        
        try:
            if ph.verify(user['password_hash'], password):
                print(f"Пользователь '{username}' авторизован")
                return user
            else:
                print("Неверный пароль")
                return None
        except VerifyMismatchError:
            print("Неверный пароль")
            return None
            
    except Exception as e:
        print(f"Ошибка при авторизации: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_users():
    """
    Получает всех пользователей
    :return: Список пользователей
    """
    conn = get_connection()
    if not conn:
        return []
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY username")
        columns = [desc[0] for desc in cursor.description]
        users = []
        for row in cursor.fetchall():
            users.append(dict(zip(columns, row)))
        return users
    except Exception as e:
        print(f"Ошибка при получении пользователей: {e}")
        return []
    finally:
        cursor.close()
        conn.close()