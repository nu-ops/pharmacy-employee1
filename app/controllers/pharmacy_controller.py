from sqlmodel import select, Session
from typing import List, Optional
from models.pharmacy import Pharmacy

def add_pharmacy(session: Session, address: str, city: str, phone: Optional[str]) -> Optional[Pharmacy]:
    """
    Добавляет новую аптеку в базу данных
    """
    try:
        pharmacy = Pharmacy(
            address=address,
            city=city,
            phone=phone
        )
        session.add(pharmacy)
        session.commit()
        session.refresh(pharmacy)
        print(f"Аптека по адресу '{address}' добавлена")
        return pharmacy
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении аптеки: {e}")
        return None

def get_all_pharmacies(session: Session) -> List[Pharmacy]:
    """
    Получает все аптеки из базы данных
    """
    try:
        statement = select(Pharmacy).order_by(Pharmacy.city, Pharmacy.address)
        pharmacies = session.exec(statement).all()
        return pharmacies
    except Exception as e:
        print(f"Ошибка при получении аптек: {e}")
        return []

def del_pharmacy(session: Session, id: int) -> bool:
    """
    Удаляет аптеку по указанному ID
    """
    try:
        pharmacy = session.get(Pharmacy, id)
        if pharmacy:
            session.delete(pharmacy)
            session.commit()
            print(f"Аптека с ID '{id}' удалена")
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Ошибка при удалении аптеки: {e}")
        return False