import os
import re

def check_files_and_folders_in_directory(directory):
    invalid_chars_pattern = r'^[A-Z]+$'
    for root, dirs, files in os.walk(directory):
        for name in files:
            if re.search(invalid_chars_pattern, name):
                print(f"Найдено недопустимое имя файла: {name}")
        for name in dirs:
            if re.search(invalid_chars_pattern, name):
                print(f"Найдено недопустимое имя папки: {name}")
