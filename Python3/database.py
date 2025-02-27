import csv
import copy
from datetime import datetime
from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, username, password, role):
        self.username = username
        self.password = password 
        self.role = role
        self.created_at = datetime.now().strftime('%Y-%m-%d')

    def display_info(self):
        pass

class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password, "user")
        self.history = []

    def add_to_history(self, item):
        self.history.append(item)

    def display_info(self):
        print(f"Клиент: {self.username}, История покупок: {self.history}")

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")

    def display_info(self):
        print(f"Администратор: {self.username}, Доступ к управлению магазином")

class Database:
    Users_file = "users.csv"
    Shoes_file = "shoes.csv"

    def __init__(self):
        self._users = self.load_users()
        self._shoes = self.load_shoes()

    def load_shoes(self):
        shoes = []
        try:
            with open(self.Shoes_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    print(f"Загруженная строка: {row}")
                    if "id" in row and "brand" in row and "size" in row:
                        shoes.append({
                            "id": int(row["id"]),
                            "brand": row["brand"],
                            "model": row["model"],
                            "size": int(row["size"]),
                            "price": float(row["price"]),
                            "rating": float(row["rating"]),
                        })
                    else:
                        print(f"Ошибка: отсутствуют необходимые ключи в строке {row}")
        except FileNotFoundError:
            print(f"Файл {self.Shoes_file} не найден, создаю пустой список обуви.")
        except Exception as e:
            print(f"Ошибка при загрузке обуви: {e}")

        return shoes

    def save_users(self):
        with open(self.Users_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password", "role", "created_at"])
            for user in self._users:
                writer.writerow([user.username, user.password, user.role, user.created_at])

    def load_shoes(self):
        shoes = []
        try:
            with open(self.Shoes_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    shoes.append({
                        "id": int(row["id"]),
                        "brand": row["brand"],
                        "model": row["model"],
                        "size": int(row["size"]),
                        "price": float(row["price"]),
                        "rating": float(row["rating"])
                    })
        except FileNotFoundError:
            print(f"Файл {self.Shoes_file} не найден. Будет создан новый при сохранении.")
        return shoes
    
    def load_users(self):
        users = []
        try:
            with open(self.Users_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if "username" in row and "password" in row and "role" in row:
                        if row["role"] == "admin":
                            users.append(Admin(row["username"], row["password"]))
                        else:
                            users.append(Customer(row["username"], row["password"]))
                    else:
                        print(f" Ошибка в строке: {row}")
        except FileNotFoundError:
            print(f" Файл {self.Users_file} не найден, создаю пустой список пользователей.")
        except Exception as e:
            print(f" Ошибка при загрузке пользователей: {e}")
        
        return users

    def save_shoes(self):
        with open(self.Shoes_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "brand", "model", "size", "price", "rating"])
            for shoe in self._shoes:
                writer.writerow([shoe["id"], shoe["brand"], shoe["model"], shoe["size"], shoe["price"], shoe["rating"]])

    def authenticate_user(self, username, password):
        for user in self._users:
            if user.username == username and user.password == password:
                print("Успешный вход!")
                return True
        print("Ошибка: Неверный логин или пароль.")
        return False

    def add_user(self, username, password, role="user"):
        if any(user.username == username for user in self._users):
            print("Ошибка: пользователь уже существует!")
            return False
        new_user = Customer(username, password) if role == "user" else Admin(username, password)
        self._users.append(new_user)
        self.save_users()
        print("Пользователь успешно добавлен!")
        return True

    def delete_user(self, username):
        self._users = [user for user in self._users if user.username != username]
        self.save_users()
        print(f"Пользователь {username} удален.")

    def get_users(self):
        return copy.deepcopy(self._users)

    def find_user(self, username, password):
        for user in self._users:
            if user.username == username and user.password == password:
                return user
        return None

    def add_shoe(self, brand, model, size, price, rating):
        new_shoe = {
            "id": max([shoe["id"] for shoe in self._shoes], default=0) + 1,
            "brand": brand,
            "model": model,
            "size": size,
            "price": price,
            "rating": rating
        }
        self._shoes.append(new_shoe)
        self.save_shoes()
        print("Товар успешно добавлен!")

    def delete_shoe(self, shoe_id):
        self._shoes = [shoe for shoe in self._shoes if shoe["id"] != shoe_id]
        self.save_shoes()
        print("Товар успешно удален!")

    def search_shoes(self, brand, size):
        return [shoe for shoe in self._shoes if shoe["brand"] == brand and shoe["size"] == size]

    def sort_shoes_by_price(self):
        return sorted(self._shoes, key=lambda shoe: shoe["price"])

    def show_users(self):
        for user in self._users:
            print(f"Пользователь: {user.username}, Пароль: {user.password}, Роль: {user.role}")
    
    def get_shoes(self):
        return self._shoes.copy()

    def export_shoes(self, filename="shoes_export.csv"):
        try:
            with open(filename, mode= 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "brand", "model", "size", "price","rating"])
                for shoe in self._shoes:
                    writer.writerow([shoe['id'], shoe['brand'], shoe['model'], shoe['size'], shoe['price'], shoe['rating']])
            print(f"Данные обуви экспортированы в {filename}")
        except Exception as e:
            print(f"Ошибки при экспорте обуви: {e}")

    def import_shoes(self, filename="shoes_export.csv"):
        try:
            with open(filename, mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self._shoes = [
                    {
                        "id": int(row['id']),
                        "brand": row["brand"],
                        "model": row["model"],
                        "size": int(row["size"]),
                        "price": float(row["price"]),
                        "rating": float(row["rating"]),
                    }
                    for row in reader
                ]
            print(f"Данные обуви загружены из {filename}")
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден. Будет создан новый при сохранении.")
        except Exception as e:
            print(f"Ошибка при загрузке обуви: {e}")

