from db.database import get_connection

def add_supplier(name, contact_person, phone, email):
    """
    Добавляет нового поставщика в базу данных
    :param name: Название поставщика
    :param contact_person: Контактное лицо
    :param phone: Телефон поставщика
    :param email: Email поставщика
    :return: True если поставщик успешно добавлен, False в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO suppliers (name, contact_person, phone, email)
            VALUES (%s, %s, %s, %s)
        """, (name, contact_person, phone, email))
        conn.commit()
        print(f"Поставщик '{name}' добавлен")
        return True
    except Exception as e:
        print(f"Ошибка при добавлении поставщика: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_suppliers():
    """
    Получает всех поставщиков из базы данных
    :return: Список всех поставщиков или пустой список в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM suppliers ORDER BY name")
        columns = [desc[0] for desc in cursor.description]
        suppliers = []
        for row in cursor.fetchall():
            suppliers.append(dict(zip(columns, row)))
        return suppliers
    except Exception as e:
        print(f"Ошибка при получении поставщиков: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def del_suppliers(id):
    """
    Удаляет поставщика по указанному ID
    :param id: ID поставщика для удаления
    :return: True если поставщик успешно удален, False в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM suppliers WHERE id = %s", (id,))
        conn.commit()
        print(f"Поставщик с ID '{id}' удален")
        return True
    except Exception as e:
        print(f"Ошибка при удалении поставщика: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update_contact_person(id, new_contact_person):
    """
    Изменяет контактное лицо поставщика по ID.
    :param id: ID поставщика
    :param new_contact_person: Новое контактное лицо
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE suppliers SET contact_person = %s WHERE id = %s", (new_contact_person, id))
        
        if cursor.rowcount == 0:
            print("Поставщик с таким ID не найден.")
        else:
            conn.commit()
            print(f"Контактное лицо изменено на: '{new_contact_person}'")
            
    except Exception as e:
        print(f"Ошибка при обновлении: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()