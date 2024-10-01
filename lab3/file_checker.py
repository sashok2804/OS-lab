import os
import re
from tkinter import messagebox


def check_files_and_folders_in_directory(directory):
    invalid_files_and_folders = []
    valid_pattern = re.compile(r'^[A-Z]+$')  # Только буквы A-Z

    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if not valid_pattern.match(dir_name):
                invalid_files_and_folders.append(os.path.join(root, dir_name))

        for file_name in files:
            if not valid_pattern.match(file_name.split('.')[0]):
                invalid_files_and_folders.append(os.path.join(root, file_name))

    if invalid_files_and_folders:
        result = "Найдены файлы и папки с недопустимыми символами:\n" + "\n".join(invalid_files_and_folders)
    else:
        result = "Все файлы и папки соответствуют требованиям."
    messagebox.showinfo("Результат проверки", result)
