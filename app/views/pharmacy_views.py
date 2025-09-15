def show_pharmacies(pharmacies):
    if not pharmacies:
        print("Нет аптек")
        return
    
    print("\nСПИСОК АПТЕК")
    print(f"{'ID':<4} {'Город':<15} {'Адрес':<30} {'Телефон':<12}")
    
    for pharmacy in pharmacies:
        print(f"{pharmacy['id']:<4} {pharmacy['city']:<15} {pharmacy['address']:<30} {pharmacy['phone'] or '-':<12}")