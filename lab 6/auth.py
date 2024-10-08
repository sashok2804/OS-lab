import os
import logging
from tkinter import messagebox

# Настройка логирования
logging.basicConfig(filename="security_events.log", level=logging.INFO, format='%(asctime)s - %(message)s')

# Базовые данные для аутентификации
USER_CREDENTIALS = {"User": "user_password"}
CERTIFICATE_NAME = "admin_cert.pem"  # Имя цифрового сертификата Admin

# Аутентификация для User
def authenticate_user(username, password):
    if USER_CREDENTIALS.get(username) == password:
        logging.info(f"User '{username}' аутентифицирован.")
        return True
    logging.warning(f"Неудачная попытка входа для User '{username}'.")
    return False

# Аутентификация для Admin с проверкой имени сертификата
def authenticate_admin(cert_path):
    cert_file_name = os.path.basename(cert_path)  # Извлекаем имя файла из полного пути
    if cert_file_name == CERTIFICATE_NAME:
        logging.info("Admin аутентифицирован с использованием сертификата.")
        return True
    logging.warning("Неудачная попытка аутентификации Admin.")
    return False

# Авторизация пользователя для ограничения функционала
def is_admin(role):
    return role == "Admin"

def is_user(role):
    return role == "User"
