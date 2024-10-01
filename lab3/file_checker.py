import os
import re
import logging
from tkinter import messagebox

# Настройка логирования
logging.basicConfig(filename="invalid_files_and_folders.log", level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def check_files_and_folders_in_directory(directory):
    invalid_files_and_folders = []
    total_files_and_folders = 0  # Считаем общее количество файлов и папок
    valid_pattern = re.compile(r'^[A-Z]+$')  # Только буквы A-Z

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
        logging.info("Найдены файлы и папки с недопустимыми символами:")
        for item in invalid_files_and_folders:
            logging.info(item)

    # Формируем результат для отображения в интерфейсе
    invalid_count = len(invalid_files_and_folders)
    valid_count = total_files_and_folders - invalid_count

    result_message = (
        f"Проверено объектов: {total_files_and_folders}.\n"
        f"Файлов и папок с недопустимыми символами: {invalid_count}.\n"
        f"Корректных файлов и папок: {valid_count}.\n"
        f"Подробности записаны в лог файл."
    )

    # Выводим результат пользователю
    messagebox.showinfo("Результат проверки", result_message)
