def show_suppliers(suppliers):
    if not suppliers:
        print("Нет поставщиков")
        return
    
    print("\nСПИСОК ПОСТАВЩИКОВ")
    print(f"{'ID':<4} {'Название':<20} {'Контакт':<15} {'Телефон':<12} {'Email':<20}")
    
    for supplier in suppliers:
        print(f"{supplier['id']:<4} {supplier['name']:<20} {supplier['contact_person'] or '-':<15} "
              f"{supplier['phone'] or '-':<12} {supplier['email'] or '-':<20}")