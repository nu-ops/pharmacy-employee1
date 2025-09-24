from sqlmodel import select, Session
from typing import List, Optional
from datetime import date
from models.sale import Sale
from models.drug import Drug
from controllers.drug_controller import update_drug_quantity

def add_sale(session: Session, drug_id: int, quantity: int) -> Optional[Sale]:
    """
    Добавляет продажу препарата в базу данных
    """
    try:
        # Получаем препарат
        drug = session.get(Drug, drug_id)
        if not drug:
            print("Препарат не найден")
            return None
        
        if drug.quantity < quantity:
            print("Недостаточно препарата на складе")
            return None
        
        # Использование скидочной цены если есть, иначе обычную
        sale_price = drug.discount_price if drug.discount_price else drug.price
        total_price = sale_price * quantity

        sale = Sale(
            drug_id=drug_id,
            quantity=quantity,
            sale_price=sale_price
        )
        session.add(sale)
        
        # Обновляем количество препарата
        update_drug_quantity(session, drug_id, -quantity)
        
        session.commit()
        session.refresh(sale)
        print(f"Продажа добавлена. Общая сумма: {total_price}")
        return sale
        
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении продажи: {e}")
        return None

def get_all_sales(session: Session) -> List[Sale]:
    """
    Получает все продажи из базы данных
    """
    try:
        statement = select(Sale).order_by(Sale.sale_date.desc())
        sales = session.exec(statement).all()
        return sales
    except Exception as e:
        print(f"Ошибка при получении продаж: {e}")
        return []

def get_sales_by_date(session: Session, start_date: date, end_date: date) -> List[Sale]:
    """
    Получает продажи за указанный период времени
    """
    try:
        from sqlmodel import and_
        statement = select(Sale).where(
            and_(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            )
        ).order_by(Sale.sale_date.desc())
        sales = session.exec(statement).all()
        return sales
    except Exception as e:
        print(f"Ошибка при получении продаж: {e}")
        return []