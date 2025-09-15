def show_drugs(drugs):
    if not drugs:
        print("Нет препаратов в базе")
        return
    
    print("\nСПИСОК ПРЕПАРАТОВ")
    print(f"{'ID':<4} {'Название':<30} {'АТК код':<12} {'Цена':<8} {'Скидка':<8} {'Кол-во':<6}")

    for drug in drugs:
        discount = drug['discount_price'] if drug['discount_price'] else "-"
        print(f"{drug['id']:<4} {drug['name']:<30} {drug['atc_code'] or '-':<12} "
              f"{drug['price']:<8} {discount:<8} {drug['quantity']:<6}")

def show_drug_details(drug, properties):
    print(f"\nДЕТАЛИ ПРЕПАРАТА: {drug['name']}")
    print(f"ID: {drug['id']}")
    print(f"АТК код: {drug['atc_code'] or 'Не указан'}")
    print(f"Цена: {drug['price']}")
    print(f"Скидочная цена: {drug['discount_price'] or 'Нет'}")
    print(f"Количество: {drug['quantity']}")
    print(f"Описание: {drug['description'] or 'Нет описания'}")
    
    if properties:
        print("\nСвойства:")
        for prop in properties:
            print(f"  {prop['property_name']}: {prop['property_value']}")

