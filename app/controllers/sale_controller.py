from db.database import get_connection
from controllers.drug_controller import update_drug_quantity

def add_sale(drug_id, quantity):
    """
    Добавляет продажу препарата в базу данных
    :param drug_id: ID продаваемого препарата
    :param quantity: Количество продаваемого препарата
    :return: True если продажа успешно добавлена, False в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT price, discount_price, quantity FROM drugs WHERE id = %s", (drug_id,))
        row = cursor.fetchone()
        
        if not row:
            print("Препарат не найден")
            return False
        
        # Преобразуем в словарь
        columns = [desc[0] for desc in cursor.description]
        drug = dict(zip(columns, row))
        
        if drug['quantity'] < quantity:
            print("Недостаточно препарата на складе")
            return False
        
        # использование скидочной цены если есть, иначе обычную
        sale_price = drug['discount_price'] if drug['discount_price'] else drug['price']
        total_price = sale_price * quantity

        cursor.execute("""
            INSERT INTO sales (drug_id, quantity, sale_price)
            VALUES (%s, %s, %s)
        """, (drug_id, quantity, sale_price))
        
        update_drug_quantity(drug_id, -quantity)
        
        conn.commit()
        print(f"Продажа добавлена. Общая сумма: {total_price}")
        return True
        
    except Exception as e:
        print(f"Ошибка при добавлении продажи: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_sales():
    """
    Получает все продажи из базы данных
    :return: Список всех продаж или пустой список в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT s.*, d.name as drug_name 
            FROM sales s 
            JOIN drugs d ON s.drug_id = d.id 
            ORDER BY s.sale_date DESC
        """)
        columns = [desc[0] for desc in cursor.description]
        sales = []
        for row in cursor.fetchall():
            sales.append(dict(zip(columns, row)))
        return sales
    except Exception as e:
        print(f"Ошибка при получении продаж: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_sales_by_date(start_date, end_date):
    """
    Получает продажи за указанный период времени
    :param start_date: Начальная дата периода
    :param end_date: Конечная дата периода
    :return: Список продаж за указанный период или пустой список в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT s.*, d.name as drug_name 
            FROM sales s 
            JOIN drugs d ON s.drug_id = d.id 
            WHERE date(s.sale_date) BETWEEN %s AND %s
            ORDER BY s.sale_date DESC
        """, (start_date, end_date))
        columns = [desc[0] for desc in cursor.description]
        sales = []
        for row in cursor.fetchall():
            sales.append(dict(zip(columns, row)))
        return sales
    except Exception as e:
        print(f"Ошибка при получении продаж: {e}")
        return []
    finally:
        cursor.close()
        conn.close()