from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from db.database import init_db, get_session
from controllers import (drug_controller, sale_controller, supplier_controller, 
                        pharmacy_controller, user_controller)
from views import drug_views, pharmacy_views, sale_views, supplier_views, user_views

current_user = None

def main():
    engine = init_db()
    if not engine:
        print("Не удалось подключиться к базе данных. Завершение работы.")
        return
    
    print("Система учета аптечных препаратов")

    if not login_menu():
        return
    
    while True:
        print(f"\nГЛАВНОЕ МЕНЮ (Пользователь: {current_user.username} - {current_user.role})")
        print("1. Препараты")
        print("2. Продажи")
        print("3. Поставщики")
        print("4. Аптеки")
        if current_user.role == 'admin':
            print("5. Пользователи")
            print("6. Выход")
        else:
            print("5. Выход")
        
        choice = input("Выберите раздел: ").strip()

        if choice == "1":
            drug_menu()
        elif choice == "2":
            sale_menu()
        elif choice == "3":
            supplier_menu()
        elif choice == "4":
            pharmacy_menu()
        elif choice == "5" and current_user.role == 'admin':
            user_menu()
        elif (choice == "6" and current_user.role == 'admin') or (choice == "5" and current_user.role != 'admin'):
            print("Завершение работы")
            break
        else:
            print("Неверный выбор")

def login_menu():
    """
    Меню авторизации и регистрации
    """
    global current_user
    
    with get_session() as session:
        while True:
            print("\n СИСТЕМА АВТОРИЗАЦИИ")
            print("1. Вход")
            print("2. Регистрация")
            print("3. Выход")
            
            choice = input("Выберите действие: ").strip()
            
            if choice == "1":
                username = input("Имя пользователя: ").strip()
                password = input("Пароль: ").strip()
                
                user = user_controller.authorize_user(session, username, password)
                if user:
                    current_user = user
                    return True
                else:
                    print("Ошибка авторизации. Проверьте логин и пароль.")
                    
            elif choice == "2":
                username = input("Придумайте имя пользователя: ").strip()
                password = input("Придумайте пароль: ").strip()
                
                if len(password) < 6:
                    print("Пароль должен содержать минимум 6 символов")
                    continue
                    
                if user_controller.register_user(session, username, password):
                    print("Теперь войдите в систему со своими учетными данными")
                else:
                    print("Ошибка регистрации. Возможно, пользователь с таким именем уже существует.")
                    
            elif choice == "3":
                print("До свидания!")
                return False
                
            else:
                print("Неверный выбор")

def user_menu():
    """
    Меню управления пользователями (только для администраторов)
    """
    with get_session() as session:
        while True:
            print("\nУПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ")
            print("1. Показать всех пользователей")
            print("2. Назад")
            
            choice = input("Выберите действие: ").strip()
            
            if choice == "1":
                users = user_controller.get_all_users(session)
                user_views.show_users(users)
            elif choice == "2":
                break
            else:
                print("Неверный выбор")

def drug_menu():
    with get_session() as session:
        while True:
            print("\nУПРАВЛЕНИЕ ПРЕПАРАТАМИ")
            print("1. Показать все препараты")
            print("2. Добавить препарат")
            print("3. Показать детали препарата")
            print("4. Добавить свойство препарата")
            print("5. Назад")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                drugs = drug_controller.get_all_drugs(session)
                drug_views.show_drugs(drugs)
            
            elif choice == "2":
                print("\nДобавление препарата:")
                name = input("Название: ").strip()
                if not name:
                    print("Название не может быть пустым")
                    continue
                    
                atc_code = input("АТК код: ").strip() or None
                description = input("Описание: ").strip() or None
                try:
                    price = float(input("Цена: ").strip())
                    discount_input = input("Скидочная цена (Enter если нет): ").strip()
                    discount_price = float(discount_input) if discount_input else None
                    quantity = int(input("Количество: ").strip())
                    
                    drug = drug_controller.add_drug(session, name, atc_code, description, price, discount_price, quantity)
                    if drug:
                        print("Препарат успешно добавлен")
                    else:
                        print("Ошибка при добавлении препарата")
                except ValueError:
                    print("Ошибка: введите корректные числовые значения для цены и количества")
                except Exception as e:
                    print(f"Ошибка при добавлении препарата: {e}")
                
            elif choice == "3":
                drug_id = input("ID препарата: ").strip()
                if drug_id.isdigit():
                    drug = drug_controller.get_drug_by_id(session, int(drug_id))
                    if drug:
                        properties = drug_controller.get_drug_properties(session, int(drug_id))
                        drug_views.show_drug_details(drug, properties)
                    else:
                        print("Препарат не найден")
                else:
                    print("Введите корректный ID")
            
            elif choice == "4":
                drug_id = input("ID препарата: ").strip()
                if drug_id.isdigit():
                    prop_name = input("Название свойства: ").strip()
                    prop_value = input("Значение свойства: ").strip()
                    if prop_name and prop_value:
                        success = drug_controller.add_drug_property(session, int(drug_id), prop_name, prop_value)
                        if success:
                            print("Свойство успешно добавлено")
                        else:
                            print("Ошибка при добавлении свойства")
                    else:
                        print("Название и значение свойства не могут быть пустыми")
                else:
                    print("Введите корректный ID")
            
            elif choice == "5":
                break
            else:
                print("Неверный выбор")

def sale_menu():
    with get_session() as session:
        while True:
            print("\nУПРАВЛЕНИЕ ПРОДАЖАМИ")
            print("1. Показать все продажи")
            print("2. Добавить продажу")
            print("3. Показать продажи за период")
            print("4. Назад")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                sales = sale_controller.get_all_sales(session)
                sale_views.show_sales(sales)

            elif choice == "2":
                print("\nДобавление продажи:")
                drug_id = input("ID препарата: ").strip()
                quantity = input("Количество: ").strip()
                if drug_id.isdigit() and quantity.isdigit():
                    sale = sale_controller.add_sale(session, int(drug_id), int(quantity))
                    if sale:
                        print("Продажа успешно добавлена")
                    else:
                        print("Не удалось добавить продажу")
                else:
                    print("Введите корректные данные")
            
            elif choice == "3":
                start_date = input("Начальная дата (ГГГГ-ММ-ДД): ").strip()
                end_date = input("Конечная дата (ГГГГ-ММ-ДД): ").strip()
                
                try:
                    start = datetime.strptime(start_date, "%Y-%m-%d").date()
                    end = datetime.strptime(end_date, "%Y-%m-%d").date()
                    sales = sale_controller.get_sales_by_date(session, start, end)
                    sale_views.show_sales(sales)
                except ValueError:
                    print("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            
            elif choice == "4":
                break
            else:
                print("Неверный выбор")

def supplier_menu():
    with get_session() as session:
        while True:
            print("\nУПРАВЛЕНИЕ ПОСТАВЩИКАМИ")
            print("1. Показать всех поставщиков")
            print("2. Добавить поставщика")
            print("3. Изменить контактное лицо поставщика")
            print("4. Удалить поставщика")
            print("5. Назад")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                suppliers = supplier_controller.get_all_suppliers(session)
                supplier_views.show_suppliers(suppliers)
            
            elif choice == "2":
                print("\nДобавление поставщика:")
                name = input("Название: ").strip()
                if not name:
                    print("Название не может быть пустым")
                    continue
                contact_person = input("Контактное лицо: ").strip() or None
                phone = input("Телефон: ").strip() or None
                email = input("Email: ").strip() or None
                supplier = supplier_controller.add_supplier(session, name, contact_person, phone, email)
                if supplier:
                    print("Поставщик успешно добавлен")
                else:
                    print("Не удалось добавить поставщика")

            elif choice == "3":
                suppliers = supplier_controller.get_all_suppliers(session)
                if suppliers:
                    supplier_views.show_suppliers(suppliers)
                    try:
                        id = int(input("Введите ID поставщика для изменения контактного лица: "))
                        new_contact_person = input("Новое контактное лицо: ").strip()
                        if new_contact_person:
                            success = supplier_controller.update_contact_person(session, id, new_contact_person)
                            if success:
                                print("Контактное лицо успешно изменено")
                            else:
                                print("Не удалось изменить контактное лицо")
                        else:
                            print("Контактное лицо не может быть пустым")
                    except ValueError:
                        print("Введите корректный ID.")
                else:
                    print("Нет поставщиков для изменения")
            
            elif choice == "4":
                suppliers = supplier_controller.get_all_suppliers(session)
                if suppliers:
                    supplier_views.show_suppliers(suppliers)
                    id_input = input("Введите ID поставщика для удаления: ").strip()
                    if id_input.isdigit():
                        success = supplier_controller.del_supplier(session, int(id_input))
                        if success:
                            print("Поставщик успешно удален")
                        else:
                            print("Не удалось удалить поставщика")
                    else:
                        print("Введите корректный ID")
                else:
                    print("Нет поставщиков для удаления")

            elif choice == "5":
                break
            else:
                print("Неверный выбор")

def pharmacy_menu():
    with get_session() as session:
        while True:
            print("\nУПРАВЛЕНИЕ АПТЕКАМИ")
            print("1. Показать все аптеки")
            print("2. Добавить аптеку")
            print("3. Удалить аптеку")
            print("4. Назад")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                pharmacies = pharmacy_controller.get_all_pharmacies(session)
                pharmacy_views.show_pharmacies(pharmacies)
            
            elif choice == "2":
                print("\nДобавление аптеки:")
                address = input("Адрес: ").strip()
                city = input("Город: ").strip()
                if not address or not city:
                    print("Адрес и город не могут быть пустыми")
                    continue  
                phone = input("Телефон: ").strip() or None
                pharmacy = pharmacy_controller.add_pharmacy(session, address, city, phone)
                if pharmacy:
                    print("Аптека успешно добавлена")
                else:
                    print("Не удалось добавить аптеку")

            elif choice == "3":
                pharmacies = pharmacy_controller.get_all_pharmacies(session)
                if pharmacies:
                    pharmacy_views.show_pharmacies(pharmacies)
                    id_input = input("Введите ID аптеки для удаления: ").strip()
                    if id_input.isdigit():
                        success = pharmacy_controller.del_pharmacy(session, int(id_input))
                        if success:
                            print("Аптека успешно удалена")
                        else:
                            print("Не удалось удалить аптеку")
                    else:
                        print("Введите корректный ID")
                else:
                    print("Нет аптек для удаления")
            
            elif choice == "4":
                break
            else:
                print("Неверный выбор")

if __name__ == "__main__":
    main()