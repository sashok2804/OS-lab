import os
import re
import logging
from tkinter import messagebox

# Создание отдельного логгера для этого модуля
checker_logger = logging.getLogger("checker_logger")
checker_logger.setLevel(logging.INFO)
checker_handler = logging.FileHandler("invalid_files_and_folders.log")
checker_formatter = logging.Formatter('%(asctime)s - %(message)s')
checker_handler.setFormatter(checker_formatter)
checker_logger.addHandler(checker_handler)

def check_files_and_folders_in_directory(directory):
    invalid_files_and_folders = []
    total_files_and_folders = 0  # Считаем общее количество файлов и папок
    valid_pattern = re.compile(r'^[A-Z]+')  # Паттерн для валидных имен

    # Обходим директорию и проверяем имена файлов и папок
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            total_files_and_folders += 1
            if not valid_pattern.match(dir_name):
                invalid_files_and_folders.append(os.path.join(root, dir_name))

        for file_name in files:
            total_files_and_folders += 1
            if not valid_pattern.match(file_name.split('.')[0]):  # Проверяем имя без расширения
                invalid_files_and_folders.append(os.path.join(root, file_name))

    # Записываем в лог-файл пути недопустимых файлов и папок
    if invalid_files_and_folders:
        checker_logger.info("Найдены файлы и папки с недопустимыми символами:")
        for item in invalid_files_and_folders:
            checker_logger.info(item)

    # Формируем результат для отображения в интерфейсе
    invalid_count = len(invalid_files_and_folders)
    valid_count = total_files_and_folders - invalid_count

    result_message = (
        f"Проверено объектов: {total_files_and_folders}.\n"
        f"Файлов и папок с недопустимыми символами: {invalid_count}.\n"
        f"Корректных файлов и папок: {valid_count}.\n"
        f"Подробности записаны в лог файл."
    )

    messagebox.showinfo("Результат проверки", result_message)
