import os
import re

def check_files_in_directory(directory):
    invalid_files = []
    valid_pattern = re.compile(r'^[A-Z]+$')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if not valid_pattern.match(file.split('.')[0]):
                invalid_files.append(os.path.join(root, file))

    if invalid_files:
        print("Найдено файлы с недопустимыми символами:")
        for invalid_file in invalid_files:
            print(invalid_file)
    else:
        print("Все файлы соответствуют требованиям.")
