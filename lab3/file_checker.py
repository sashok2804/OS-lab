import os
import re

def check_files_and_folders_in_directory(directory):
    invalid_files_and_folders = []
    valid_pattern = re.compile(r'^[A-Z]+$')  # Только буквы A-Z

    for root, dirs, files in os.walk(directory):
        # Проверяем папки
        for dir_name in dirs:
            if not valid_pattern.match(dir_name):
                invalid_files_and_folders.append(os.path.join(root, dir_name))
        
        # Проверяем файлы
        for file_name in files:
            if not valid_pattern.match(file_name.split('.')[0]):
                invalid_files_and_folders.append(os.path.join(root, file_name))

    if invalid_files_and_folders:
        print("Найдены файлы и папки с недопустимыми символами:")
        for item in invalid_files_and_folders:
            print(item)
    else:
        print("Все файлы и папки соответствуют требованиям.")
