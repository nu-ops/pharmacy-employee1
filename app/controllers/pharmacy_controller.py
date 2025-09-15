from db.database import get_connection

def add_pharmacy(address, city, phone):
    """
    Добавляет новую аптеку в базу данных
    :param address: Адрес аптеки
    :param city: Город, в котором находится аптека
    :param phone: Телефон аптеки
    :return: True если аптека успешно добавлена, False в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO pharmacies (address, city, phone)
            VALUES (%s, %s, %s)
        """, (address, city, phone))
        conn.commit()
        print(f"Аптека по адресу '{address}' добавлена")
        return True
    except Exception as e:
        print(f"Ошибка при добавлении аптеки: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_pharmacies():
    """
    Получает все аптеки из базы данных
    :return: Список всех аптек или пустой список в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pharmacies ORDER BY city, address")
        columns = [desc[0] for desc in cursor.description]
        pharmacies = []
        for row in cursor.fetchall():
            pharmacies.append(dict(zip(columns, row)))
        return pharmacies
    except Exception as e:
        print(f"Ошибка при получении аптек: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def del_pharmacy(id):
    """
    Удаляет аптеку по указанному ID
    :param id: ID аптеки для удаления
    :return: True если аптека успешно удалена, False в случае ошибки
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pharmacies WHERE id = %s", (id,))
        conn.commit()
        print(f"Аптека с ID '{id}' удалена")
        return True
    except Exception as e:
        print(f"Ошибка при удалении аптеки: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()