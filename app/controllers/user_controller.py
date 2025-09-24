from sqlmodel import select, Session
from typing import List, Optional
from argon2.exceptions import VerifyMismatchError
from models.user import User
from db.database import ph

def register_user(session: Session, username: str, password: str, role: str = "user") -> Optional[User]:
    """
    Регистрирует нового пользователя
    """
    try:
        password_hash = ph.hash(password)
        user = User(
            username=username,
            password_hash=password_hash,
            role=role
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"Пользователь '{username}' успешно зарегистрирован")
        return user
    except Exception as e:
        session.rollback()
        print(f"Ошибка при регистрации: {e}")
        return None

def authorize_user(session: Session, username: str, password: str) -> Optional[User]:
    """
    Авторизует пользователя
    """
    try:
        user = get_user_by_username(session, username)
        if not user:
            print("Пользователь не найден")
            return None
        
        try:
            if ph.verify(user.password_hash, password):
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

def get_all_users(session: Session) -> List[User]:
    """
    Получает всех пользователей
    """
    try:
        statement = select(User).order_by(User.username)
        users = session.exec(statement).all()
        return users
    except Exception as e:
        print(f"Ошибка при получении пользователей: {e}")
        return []

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """
    Получает пользователя по имени пользователя
    """
    try:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()
    except Exception as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None