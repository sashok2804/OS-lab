import os
import random
import string

def create_root_folder(drive):
    folder_name = "RootFolder"
    path = os.path.join(drive, folder_name)
    
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Папка {path} успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании папки: {e}")

def generate_random_files_and_folders(base_path):
    try:
        for i in range(3):  # Генерация 3 папок
            folder_name = "Folder_" + ''.join(random.choices(string.ascii_letters, k=5))
            folder_path = os.path.join(base_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            # Генерация файлов внутри папки
            for j in range(3):  # 3 файла на каждую папку
                file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ".txt"
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'w') as f:
                    f.write("Тестовый файл")
        
        print(f"Генерация папок и файлов в {base_path} завершена.")
    except Exception as e:
        print(f"Ошибка при генерации файлов и папок: {e}")
