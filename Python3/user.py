from database import Database
from database import Customer 
from database import User

db = Database()




def user_menu(db: Database):
    print("Добро пожаловать в магазин обуви!")
    print("Пожалуйста, авторизуйтесь.")
    try:
        username = input("Логин: ")
        password = input("Пароль: ")
        user = next((u for u in db.get_users() if u.username == username), None)

        if user and user.verify_password(password):
            user.display_info()
            while True:
                print("\nВыберите действие:")
                print("1. Просмотреть каталог обуви")
                print("2. Найти обувь по параметрам")
                print("3. Сортировать обувь по цене")
                print("4. Просмотреть историю покупок")
                print("5. Обновить профиль")
                print("6. Выйти")

                choice = input("Ваш выбор: ")

                if choice == '1':
                    view_shoes(db)
                elif choice == '2':
                    search_shoes(db)
                elif choice == '3':
                    sort_shoes_by_price(db)
                elif choice == '4':
                    view_purchase_history(user)
                elif choice == '5':
                    update_profile(user)
                elif choice == '6':
                    break
                else:
                    print("Неверный выбор! Попробуйте снова.")
        else:
            print("Неверный логин или пароль.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def view_shoes(db):
    print("Каталог обуви:")
    for shoe in db.get_shoes():
        print(f"{shoe['brand']} {shoe['model']} - {shoe['size']} - {shoe['price']} - {shoe['rating']}")

def search_shoes(db: Database):
    try:
        brand = input("Введите бренд для поиска: ")
        size = int(input("Введите размер: "))
        found_shoes = db.search_shoes(brand, size)
        print("Результаты поиска:")
        if found_shoes:
            for shoe in found_shoes:
                print(f"{shoe['brand']} {shoe['model']} - {shoe['size']} - {shoe['price']} - {shoe['rating']}")
        else:
            print("Обувь не найдена.")
    except ValueError:
        print("Ошибка: размер должен быть числом.")

def sort_shoes_by_price(db):
    sorted_shoes = sorted(db.get_shoes(), key=lambda shoe: shoe['price'])
    print("Обувь, отсортированная по цене:")
    for shoe in sorted_shoes:
        print(f"{shoe['brand']} {shoe['model']} - {shoe['price']}")

def view_purchase_history(user: Customer):
    print("История ваших покупок:")
    if user.history:
        for item in user.history:
            print(item)
    else:
        print("История покупок пуста.")

def update_profile(user: User):
    new_password = input("Введите новый пароль: ")
    user.set_password(new_password)
    print("Пароль успешно обновлен!")

    