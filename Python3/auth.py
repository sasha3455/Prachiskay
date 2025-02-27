import hashlib
from database import Database

db = Database()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    password_hash = hash_password(password)
    return next((user for user in db.get_users() if user['username'] == username and user['password'] == password_hash and user['role'] == 'user'), None)

def authenticate_admin(username, password):
    password_hash = hash_password(password)
    return next((user for user in db.get_users() if user['username'] == username and user['password'] == password_hash and user['role'] == 'admin'), None)
