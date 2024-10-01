import os
import random
import string

def create_root_folder(base_path):
    root_folder = "RootFolder"
    root_path = os.path.join(base_path, root_folder)
    
    try:
        os.makedirs(root_path, exist_ok=True)
        print(f"Корневая папка создана: {root_path}")
        return root_path
    except Exception as e:
        print(f"Ошибка при создании корневой папки: {e}")
        return None

def generate_random_name(correct=True):
    if correct:
        return ''.join(random.choices(string.ascii_uppercase, k=5))
    else:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def generate_random_files_and_folders(base_path, level=0, max_level=2):
    if level > max_level:
        return
    
    try:
        for i in range(random.randint(2, 4)):  # Генерируем 2-4 элемента
            if random.choice([True, False]):  # Случайно выбираем: папка или файл
                # Генерация папки
                folder_name = generate_random_name(correct=random.choice([True, False]))
                folder_path = os.path.join(base_path, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                print(f"Создана папка: {folder_path}")
                
                # Рекурсивно создаем вложенные файлы и папки
                generate_random_files_and_folders(folder_path, level + 1, max_level)
            else:
                # Генерация файла
                file_name = generate_random_name(correct=random.choice([True, False])) + ".txt"
                file_path = os.path.join(base_path, file_name)
                with open(file_path, 'w') as f:
                    f.write("Тестовый файл")
                print(f"Создан файл: {file_path}")
                
    except Exception as e:
        print(f"Ошибка при генерации файлов и папок: {e}")
