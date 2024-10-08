import os
import random
import string

def create_root_folder(directory):
    root_folder = os.path.join(directory, "RootFolder")
    os.makedirs(root_folder, exist_ok=True)
    print(f"Корневая папка создана по пути: {root_folder}")
    
def generate_random_files_and_folders(directory):
    root_folder = os.path.join(directory, "RootFolder")
    if not os.path.exists(root_folder):
        print("Корневая папка не найдена. Создайте ее сначала.")
        return
    
    for _ in range(5):  # Генерируем 5 папок
        folder_name = ''.join(random.choices(string.ascii_letters, k=8))
        folder_path = os.path.join(root_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        for _ in range(5):  # Генерируем по 5 файлов в каждой папке
            file_name = ''.join(random.choices(string.ascii_letters, k=8)) + ".txt"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w') as f:
                f.write("Это тестовый файл.")
                
    print("Файлы и папки сгенерированы.")
