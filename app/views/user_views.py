def show_users(users):
    if not users:
        print("Нет пользователей в системе")
        return
    
    print("\nСПИСОК ПОЛЬЗОВАТЕЛЕЙ")
    print(f"{'ID':<4} {'Имя':<20} {'Роль':<10} {'Дата регистрации':<20}")
    
    for user in users:
        print(f"{user['id']:<4} {user['username']:<20} {user['role']:<10} {str(user['created_at'])[:19]:<20}")