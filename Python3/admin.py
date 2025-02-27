from database import Database
from database import Admin 
from database import User

db = Database()
shoes = db.get_shoes()
users = db.get_users()

def admin_menu():
    print("Добро пожаловать, администратор!")
    username = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")
    
    if not db.authenticate_user(username, password):
        print("Ошибка: Неверный логин или пароль.")
        return

    admin = next((user for user in db.get_users() if user.username == username), None)

    if isinstance(admin, Admin):  
        admin.display_info()
    else:
        print("Ошибка: пользователь не является администратором.")
        return

    while True:
        print("\nВыберите действие:")
        print("1. Добавить товар")
        print("2. Удалить товар")
        print("3. Управление пользователями")
        print("4. Экспортировать товары")
        print("5. Импортировать товары")
        print("6. Показать пользователей")
        print("7. Показать всю обувь")
        print("8. Выйти")

        choice = input("Ваш выбор: ")

        if choice == '1':
            add_shoe()
        elif choice == '2':
            delete_shoe()
        elif choice == '3':
            manage_users()
        elif choice == '4': 
            db.export_shoes()
        elif choice == '5':
            db.import_shoes()
        elif choice == '6':
            show_users(db)
        elif choice == '7':
            view_shoes(db)
        elif choice == '8':
            break
        else:
            print("Неверный выбор! Попробуйте снова.")

def view_shoes(db):
    print("Каталог обуви:")
    for shoe in db.get_shoes():
        print(f"{shoe['brand']} {shoe['model']} - {shoe['size']} - {shoe['price']} - {shoe['rating']}")

def add_shoe():
    try:
        brand = input("Введите бренд: ")
        model = input("Введите модель: ")
        size = int(input("Введите размер: "))
        price = float(input("Введите цену: "))
        rating = float(input("Введите рейтинг: "))

        db.add_shoe(brand, model, size, price, rating)

        print("Товар успешно добавлен!")
    except ValueError:
        print("Ошибка: введите корректные данные!")

def delete_shoe():
    try:
        brand = input("Введите бренд: ")
        model = input("Введите модель: ")
        size = int(input("Введите размер: "))
        price = float(input("Введите цену: "))
        rating = float(input("Введите рейтинг: "))

        db.delete_shoe(brand, model, size, price, rating)

        print("Товар успешно добавлен!")
    except ValueError:
        print("Ошибка: введите корректные данные!")

def manage_users():
    print("Выберите действие:")
    print("1. Добавить пользователя")
    print("2. Удалить пользователя")

    choice = input("Ваш выбор: ")

    if choice == '1':
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        role = input("Введите роль (user/admin): ").strip().lower()

        if db.add_user(username, password, role):
            print("Пользователь успешно добавлен!")
        else:
            print("Ошибка: пользователь уже существует!")

    elif choice == '2':
        username = input("Введите имя пользователя для удаления: ")

        if db.delete_user(username):
            print("Пользователь успешно удален!")
        else:
            print("Ошибка: пользователь не найден!")


def export_shoes():
    format_choice = input("Экспотр CSV (Введите 1 для эскпорта)")
    
    if format_choice == '1':
        db.export_shoes()
    else:
        print("Неверный выбор!")

def import_shoes():
    format_choice = input("Импорт СSV (Введите 1 для импорта)")
    
    if format_choice == '1':
        db.import_shoes()
    else:
        print("Неверный выбор!")

def show_users(database):
    print("\nСписок пользователей:")
    for user in database._users:
        print(f"Пользователь: {user.username}, Хеш пароля: {user.password}, Роль: {user.role}")
