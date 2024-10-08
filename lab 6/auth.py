import os
import logging
from tkinter import messagebox

# Настройка логирования
logging.basicConfig(filename="security_events.log", level=logging.INFO, format='%(asctime)s - %(message)s')

# Базовые данные для аутентификации
USER_CREDENTIALS = {"User": "user_password"}
CERTIFICATE_PATH = "admin_cert.pem"  # Путь к цифровому сертификату Admin

# Аутентификация для User
def authenticate_user(username, password):
    if USER_CREDENTIALS.get(username) == password:
        logging.info(f"User '{username}' аутентифицирован.")
        return True
    logging.warning(f"Неудачная попытка входа для User '{username}'.")
    return False

# Аутентификация для Admin с проверкой сертификата
def authenticate_admin(cert_path):
    if os.path.exists(cert_path) and cert_path == CERTIFICATE_PATH:
        logging.info("Admin аутентифицирован с использованием сертификата.")
        return True
    logging.warning("Неудачная попытка аутентификации Admin.")
    return False

# Авторизация пользователя для ограничения функционала
def is_admin(role):
    return role == "Admin"

def is_user(role):
    return role == "User"
