from db.database import get_connection

def add_drug(name, atc_code, description, price, discount_price, quantity):
    """
    Добавляет новый препарат в базу данных
    :param name: Название препарата
    :param atc_code: ATC код препарата
    :param description: Описание препарата
    :param price: Цена препарата
    :param discount_price: Скидочная цена препарата (может быть None)
    :param quantity: Количество препарата на складе
    :return: ID добавленного препарата или None в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO drugs (name, atc_code, description, price, discount_price, quantity)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (name, atc_code, description, price, discount_price, quantity))
        drug_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Препарат '{name}' добавлен с ID: {drug_id}")
        return drug_id
    except Exception as e:
        print(f"Ошибка при добавлении препарата: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def add_drug_property(drug_id, property_name, property_value):
    """
    Добавляет свойство к препарату в базу данных
    :param drug_id: ID препарата, к которому добавляется свойство
    :param property_name: Название свойства
    :param property_value: Значение свойства
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO drug_properties (drug_id, property_name, property_value)
            VALUES (%s, %s, %s)
        """, (drug_id, property_name, property_value))
        conn.commit()
        print(f"Свойство '{property_name}' добавлено к препарату ID: {drug_id}")
    except Exception as e:
        print(f"Ошибка при добавлении свойства: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_all_drugs():
    """
    Получает все препараты из базы данных
    :return: Список всех препаратов или пустой список в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM drugs ORDER BY name")
        columns = [desc[0] for desc in cursor.description]
        drugs = []
        for row in cursor.fetchall():
            drugs.append(dict(zip(columns, row)))
        return drugs
    except Exception as e:
        print(f"Ошибка при получении препаратов: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_drug_by_id(drug_id):
    """
    Получает препарат по его ID из базы данных
    :param drug_id: ID препарата для поиска
    :return: Данные препарата или None, если препарат не найден или произошла ошибка
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM drugs WHERE id = %s", (drug_id,))
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(zip(columns, row))
        return None
    except Exception as e:
        print(f"Ошибка при получении препарата: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_drug_properties(drug_id):
    """
    Получает все свойства указанного препарата из базы данных
    :param drug_id: ID препарата, для которого нужно получить свойства
    :return: Список свойств препарата или пустой список, если свойств нет или произошла ошибка
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM drug_properties WHERE drug_id = %s", (drug_id,))
        columns = [desc[0] for desc in cursor.description]
        properties = []
        for row in cursor.fetchall():
            properties.append(dict(zip(columns, row)))
        return properties
    except Exception as e:
        print(f"Ошибка при получении свойств: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def update_drug_quantity(drug_id, quantity_change):
    """
    Обновляет количество препарата на складе
    :param drug_id: ID препарата, количество которого нужно изменить
    :param quantity_change: Изменение количества (может быть положительным или отрицательным)
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE drugs SET quantity = quantity + %s WHERE id = %s", (quantity_change, drug_id))
        conn.commit()
        print(f"Количество препарата ID: {drug_id} обновлено на {quantity_change}")
    except Exception as e:
        print(f"Ошибка при обновлении количества: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()