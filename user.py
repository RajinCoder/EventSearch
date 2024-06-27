import sqlite3
import secrets
import random
import hashlib
from pwinput import pwinput
from events import display_user_options

conn = sqlite3.connect('events.db')

cursor = conn.cursor()

def get_user_credentials():
    option = input("L - login to an existing account \nS - create and account \nQ - quit \nPlease pick an option: ")
    username, password = None, None
    match option:
        case "L":
            username = input("Enter your username: ")
            password = pwinput("Enter your password: ")
            if not get_user_id(username, password):
                print("The username or password you have entered doesn't match our records")
            return get_user_id(username, password)
        case "S":
            username = input("Enter your username: ")
            password = pwinput("Enter your password: ")
            confirm_password = pwinput("Enter your password again: ")
            while password != confirm_password:
                print("The passwords didn't match")
                password = pwinput("Enter your password: ")
                confirm_password = pwinput("Enter your password again: ")
            if not add_user(username, password):
                print("An account with that username already exists")
            return add_user(username, password)
        case "Q":
            exit()
        case _:
            get_user_credentials()

def get_user_id(username, password):
    try:
        cursor.execute(f"SELECT id FROM user WHERE username = '{username}' AND password = '{hashlib.sha256(password.encode('utf-8')).hexdigest()}'")
        return cursor.fetchall()[0][0]
    except:
        return None
    
def add_user(username, password):
    cursor.execute(f"SELECT id FROM user WHERE username = '{username}'")
    if len(cursor.fetchall()) > 0:
        return None
    id = create_id()
    cursor.execute(f"INSERT INTO user (id, username, password) VALUES ({id},'{username}', '{hashlib.sha256(password.encode('utf-8')).hexdigest()}')")
    conn.commit()
    return id

def create_id():
    id = None
    id_already_exists = True
    while id_already_exists:
        id = random.randrange(1000000000,9999999999)
        cursor.execute(f'SELECT id FROM user WHERE id = {id}')
        id_already_exists = len(cursor.fetchall()) > 0
    return id

def get_user_by_id(id):
    try:
        cursor.execute(f"SELECT username FROM user WHERE id = {id}")
        return cursor.fetchall()[0][0]
    except:
        return None

def initialize_ui():
    user_id = get_user_credentials()
    while not user_id:
        user_id = get_user_credentials()
    print(f"Welcome @{get_user_by_id(user_id)}!")
    display_user_options(get_user_by_id(user_id), user_id)


initialize_ui()