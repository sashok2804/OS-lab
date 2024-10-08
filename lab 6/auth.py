import os
import logging
from tkinter import messagebox

# Создание отдельного логгера для этого модуля
auth_logger = logging.getLogger("auth_logger")
auth_logger.setLevel(logging.INFO)
auth_handler = logging.FileHandler("security_events.log")
auth_formatter = logging.Formatter('%(asctime)s - %(message)s')
auth_handler.setFormatter(auth_formatter)
auth_logger.addHandler(auth_handler)

# Базовые данные для аутентификации
USER_CREDENTIALS = {"User": "user_password"}
CERTIFICATE_NAME = "admin_cert.pem"  # Имя цифрового сертификата Admin

# Аутентификация для User
def authenticate_user(username, password):
    if USER_CREDENTIALS.get(username) == password:
        auth_logger.info(f"User '{username}' аутентифицирован.")
        return True
    auth_logger.warning(f"Неудачная попытка входа для User '{username}'.")
    return False

# Аутентификация для Admin с проверкой имени сертификата
def authenticate_admin(cert_path):
    cert_file_name = os.path.basename(cert_path)  # Извлекаем имя файла из полного пути
    if cert_file_name == CERTIFICATE_NAME:
        auth_logger.info("Admin аутентифицирован с использованием сертификата.")
        return True
    auth_logger.warning("Неудачная попытка аутентификации Admin.")
    return False

# Авторизация пользователя для ограничения функционала
def is_admin(role):
    return role == "Admin"

def is_user(role):
    return role == "User"
