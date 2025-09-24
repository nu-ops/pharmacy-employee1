def show_sales(sales):
    if not sales:
        print("Нет данных о продажах")
        return

    print("\nИСТОРИЯ ПРОДАЖ")
    print("Дата                Препарат              Кол-во  Цена     Сумма")

    total = 0
    for sale in sales:
        if sale.sale_date:
            date = sale.sale_date.strftime("%Y-%m-%d").split()[0]
        else:
            date = '-'
        
        drug_name = sale.drug.name if sale.drug else f"ID:{sale.drug_id}"
        qty = sale.quantity
        price = sale.sale_price
        amount = qty * price
        total += amount

        print(f"{date:<20} {drug_name:<25} {qty:<6} {price:<8} {amount:<8}")

    print(f"{'ИТОГО:':<51} {total:<8}")