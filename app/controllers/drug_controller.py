from sqlmodel import select, Session
from typing import List, Optional

from models.drug import Drug
from models.drug_property import DrugProperty

def add_drug(session: Session, name: str, atc_code: Optional[str], description: Optional[str], 
             price: float, discount_price: Optional[float], quantity: int) -> Optional[Drug]:
    """
    Добавляет новый препарат в базу данных
    """
    try:
        drug = Drug(
            name=name,
            atc_code=atc_code,
            description=description,
            price=price,
            discount_price=discount_price,
            quantity=quantity
        )
        session.add(drug)
        session.commit()
        session.refresh(drug)
        print(f"Препарат '{name}' добавлен с ID: {drug.id}")
        return drug
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении препарата: {e}")
        return None

def add_drug_property(session: Session, drug_id: int, property_name: str, property_value: str) -> bool:
    """
    Добавляет свойство к препарату в базу данных
    """
    try:
        property = DrugProperty(
            drug_id=drug_id,
            property_name=property_name,
            property_value=property_value
        )
        session.add(property)
        session.commit()
        print(f"Свойство '{property_name}' добавлено к препарату ID: {drug_id}")
        return True
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении свойства: {e}")
        return False

def get_all_drugs(session: Session) -> List[Drug]:
    """
    Получает все препараты из базы данных
    """
    try:
        statement = select(Drug).order_by(Drug.name)
        drugs = session.exec(statement).all()
        return drugs
    except Exception as e:
        print(f"Ошибка при получении препаратов: {e}")
        return []

def get_drug_by_id(session: Session, drug_id: int) -> Optional[Drug]:
    """
    Получает препарат по его ID из базы данных
    """
    try:
        return session.get(Drug, drug_id)
    except Exception as e:
        print(f"Ошибка при получении препарата: {e}")
        return None

def get_drug_properties(session: Session, drug_id: int) -> List[DrugProperty]:
    """
    Получает все свойства указанного препарата из базы данных
    """
    try:
        statement = select(DrugProperty).where(DrugProperty.drug_id == drug_id)
        properties = session.exec(statement).all()
        return properties
    except Exception as e:
        print(f"Ошибка при получении свойств: {e}")
        return []

def update_drug_quantity(session: Session, drug_id: int, quantity_change: int) -> bool:
    """
    Обновляет количество препарата на складе
    """
    try:
        drug = session.get(Drug, drug_id)
        if drug:
            drug.quantity += quantity_change
            session.add(drug)
            session.commit()
            session.refresh(drug)
            print(f"Количество препарата ID: {drug_id} обновлено на {quantity_change}")
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении количества: {e}")
        return False