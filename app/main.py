from db.database import init_db
from controllers import drug_controller, sale_controller, supplier_controller, pharmacy_controller, user_controller
from views import drug_views, pharmacy_views, sale_views, supplier_views, user_views

current_user = None

def main():
    conn = init_db()
    if not conn:
        print("Не удалось подключиться к базе данных. Завершение работы.")
        return
    
    print("Система учета аптечных препаратов")
    
    # Требуем авторизацию перед доступом к системе
    if not login_menu():
        conn.close()
        return
    
    while True:
        print(f"\nГЛАВНОЕ МЕНЮ (Пользователь: {current_user['username']} - {current_user['role']})")
        print("1. Препараты")
        print("2. Продажи")
        print("3. Поставщики")
        print("4. Аптеки")
        if current_user['role'] == 'admin':
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
        elif choice == "5" and current_user['role'] == 'admin':
            user_menu()
        elif (choice == "6" and current_user['role'] == 'admin') or (choice == "5" and current_user['role'] != 'admin'):
            print("Завершение работы")
            break
        else:
            print("Неверный выбор")
    
    conn.close()

def login_menu():
    """
    Меню авторизации и регистрации
    """
    global current_user
    
    while True:
        print("\n СИСТЕМА АВТОРИЗАЦИИ")
        print("1. Вход")
        print("2. Регистрация")
        print("3. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            username = input("Имя пользователя: ").strip()
            password = input("Пароль: ").strip()
            
            user = user_controller.authorize_user(username, password)
            if user:
                current_user = user
                return True
                
        elif choice == "2":
            username = input("Придумайте имя пользователя: ").strip()
            password = input("Придумайте пароль: ").strip()
            
            if len(password) < 6:
                print("Пароль должен содержать минимум 6 символов")
                continue
                
            if user_controller.register_user(username, password):
                print("Теперь войдите в систему со своими учетными данными")
                
        elif choice == "3":
            print("До свидания!")
            return False
            
        else:
            print("Неверный выбор")

def user_menu():
    """
    Меню управления пользователями (только для администраторов)
    """
    while True:
        print("\nУПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ")
        print("1. Показать всех пользователей")
        print("2. Назад")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            users = user_controller.get_all_users()
            user_views.show_users(users)
        elif choice == "2":
            break
        else:
            print("Неверный выбор")

def drug_menu():
    while True:
        print("\nУПРАВЛЕНИЕ ПРЕПАРАТАМИ")
        print("1. Показать все препараты")
        print("2. Добавить препарат")
        print("3. Показать детали препарата")
        print("4. Добавить свойство препарата")
        print("5. Назад")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == "1":
            drugs = drug_controller.get_all_drugs()
            drug_views.show_drugs(drugs)
        
        elif choice == "2":
            print("\nДобавление препарата:")
            name = input("Название: ").strip()
            atc_code = input("АТК код: ").strip() or None
            description = input("Описание: ").strip() or None
            try:
                price = float(input("Цена: ").strip())
                discount_input = input("Скидочная цена (Enter если нет): ").strip()
                discount_price = float(discount_input) if discount_input else None
                quantity = int(input("Количество: ").strip())
                
                drug_id = drug_controller.add_drug(name, atc_code, description, price, discount_price, quantity)  
            except ValueError:
                print("Ошибка: введите корректные числовые значения для цены и количества")
            except Exception as e:
                print(f"Ошибка при добавлении препарата: {e}")
            
        elif choice == "3":
            drug_id = input("ID препарата: ").strip()
            if drug_id.isdigit():
                drug = drug_controller.get_drug_by_id(int(drug_id))
                if drug:
                    properties = drug_controller.get_drug_properties(int(drug_id))
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
                    drug_controller.add_drug_property(int(drug_id), prop_name, prop_value)
                else:
                    print("Название и значение свойства не могут быть пустыми")
            else:
                print("Введите корректный ID")
        
        elif choice == "5":
            break
        else:
            print("Неверный выбор")

def sale_menu():
    while True:
        print("\nУПРАВЛЕНИЕ ПРОДАЖАМИ")
        print("1. Показать все продажи")
        print("2. Добавить продажу")
        print("3. Показать продажи за период")
        print("4. Назад")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == "1":
            sales = sale_controller.get_all_sales()
            sale_views.show_sales(sales)

        elif choice == "2":
            print("\nДобавление продажи:")
            drug_id = input("ID препарата: ").strip()
            quantity = input("Количество: ").strip()
            if drug_id.isdigit() and quantity.isdigit():
                success = sale_controller.add_sale(int(drug_id), int(quantity))
                if not success:
                    print("Не удалось добавить продажу")
            else:
                print("Введите корректные данные")
        
        elif choice == "3":
            start_date = input("Начальная дата (ГГГГ-ММ-ДД): ").strip()
            end_date = input("Конечная дата (ГГГГ-ММ-ДД): ").strip()
            # Проверка формата даты
            if len(start_date) == 10 and len(end_date) == 10:
                sales = sale_controller.get_sales_by_date(start_date, end_date)
                sale_views.show_sales(sales)
            else:
                print("Введите даты в формате ГГГГ-ММ-ДД")
        
        elif choice == "4":
            break
        else:
            print("Неверный выбор")

def supplier_menu():
    while True:
        print("\nУПРАВЛЕНИЕ ПОСТАВЩИКАМИ")
        print("1. Показать всех поставщиков")
        print("2. Добавить поставщика")
        print("3. Изменить контактное лицо поставщика")
        print("4. Удалить поставщика")
        print("5. Назад")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == "1":
            suppliers = supplier_controller.get_all_suppliers()
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
            success = supplier_controller.add_supplier(name, contact_person, phone, email)
            if success:
                print("Поставщик успешно добавлен")
            else:
                print("Не удалось добавить поставщика")

        elif choice == "3":
            suppliers = supplier_controller.get_all_suppliers()
            if suppliers:
                supplier_views.show_suppliers(suppliers)
                try:
                    id = int(input("Введите ID поставщика для изменения контактного лица: "))
                    new_contact_person = input("Новое контактное лицо: ").strip()
                    if new_contact_person:
                        supplier_controller.update_contact_person(id, new_contact_person)
                    else:
                        print("Контактное лицо не может быть пустым")
                except ValueError:
                    print("Введите корректный ID.")
            else:
                print("Нет поставщиков для изменения")
        
        elif choice == "4":
            suppliers = supplier_controller.get_all_suppliers()
            if suppliers:
                supplier_views.show_suppliers(suppliers)
                id_input = input("Введите ID поставщика для удаления: ").strip()
                if id_input.isdigit():
                    success = supplier_controller.del_suppliers(int(id_input))
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
    while True:
        print("\nУПРАВЛЕНИЕ АПТЕКАМИ")
        print("1. Показать все аптеки")
        print("2. Добавить аптеку")
        print("3. Удалить аптеку")
        print("4. Назад")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == "1":
            pharmacies = pharmacy_controller.get_all_pharmacies()
            pharmacy_views.show_pharmacies(pharmacies)
        
        elif choice == "2":
            print("\nДобавление аптеки:")
            address = input("Адрес: ").strip()
            city = input("Город: ").strip()
            if not address or not city:
                print("Адрес и город не могут быть пустыми")
                continue  
            phone = input("Телефон: ").strip() or None
            success = pharmacy_controller.add_pharmacy(address, city, phone)
            if success:
                print("Аптека успешно добавлена")
            else:
                print("Не удалось добавить аптеку")

        elif choice == "3":
            pharmacies = pharmacy_controller.get_all_pharmacies()
            if pharmacies:
                pharmacy_views.show_pharmacies(pharmacies)
                id_input = input("Введите ID аптеки для удаления: ").strip()
                if id_input.isdigit():
                    success = pharmacy_controller.del_pharmacy(int(id_input))
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