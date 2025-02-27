from auth import authenticate_user
from user import user_menu
from admin import admin_menu
from database import Database

db = Database()


def main():
    try:
        role = input("Введите роль (user/admin): ").strip().lower()
        if role == 'user':
            user_menu(db)
        elif role == 'admin':
            admin_menu()
        else:
            print("Неверная роль. Попробуйте снова.")
    except Exception as e:
        print(f"Ошибка в главном меню: {e}")

if __name__ == "__main__":
    main()

    