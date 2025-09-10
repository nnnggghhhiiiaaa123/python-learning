import os
from cryptography.fernet import Fernet


def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("key.key", "rb").read()


# Nếu chưa có key thì tạo mới
if not os.path.exists("key.key"):
    write_key()

key = load_key()
fer = Fernet(key)


def view():
    try:
        with open('password.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                print("User:", user, "| Password:",
                      fer.decrypt(passw.encode()).decode())
    except FileNotFoundError:
        print("⚠️ Chưa có file password.txt, hãy thêm mật khẩu trước.")


def add():
    name = input('Account Name: ')
    pwd = input("Password: ")

    with open('password.txt', 'a') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")


while True:
    mode = input(
        "Would you like to add a new password or view existing ones (view, add, q): "
    )
    if mode == "q":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
