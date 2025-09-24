from sqlmodel import select, Session
from typing import List, Optional
from models.supplier import Supplier

def add_supplier(session: Session, name: str, contact_person: Optional[str], 
                phone: Optional[str], email: Optional[str]) -> Optional[Supplier]:
    """
    Добавляет нового поставщика в базу данных
    """
    try:
        supplier = Supplier(
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email
        )
        session.add(supplier)
        session.commit()
        session.refresh(supplier)
        print(f"Поставщик '{name}' добавлен")
        return supplier
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении поставщика: {e}")
        return None

def get_all_suppliers(session: Session) -> List[Supplier]:
    """
    Получает всех поставщиков из базы данных
    """
    try:
        statement = select(Supplier).order_by(Supplier.name)
        suppliers = session.exec(statement).all()
        return suppliers
    except Exception as e:
        print(f"Ошибка при получении поставщиков: {e}")
        return []

def del_supplier(session: Session, id: int) -> bool:
    """
    Удаляет поставщика по указанному ID
    """
    try:
        supplier = session.get(Supplier, id)
        if supplier:
            session.delete(supplier)
            session.commit()
            print(f"Поставщик с ID '{id}' удален")
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Ошибка при удалении поставщика: {e}")
        return False

def update_contact_person(session: Session, id: int, new_contact_person: str) -> bool:
    """
    Изменяет контактное лицо поставщика по ID.
    """
    try:
        supplier = session.get(Supplier, id)
        if supplier:
            supplier.contact_person = new_contact_person
            session.add(supplier)
            session.commit()
            session.refresh(supplier)
            print(f"Контактное лицо изменено на: '{new_contact_person}'")
            return True
        else:
            print("Поставщик с таким ID не найден.")
            return False
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении: {e}")
        return False