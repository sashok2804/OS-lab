import os
from folder_manager import create_root_folder, generate_random_files_and_folders
from file_checker import check_files_and_folders_in_directory
from terminal_launcher import open_terminal

def main_menu():
    while True:
        print("\nМеню:")
        print("1. Создать корневую папку")
        print("2. Генерировать файлы и папки для проверки")
        print("3. Проверить файлы и папки на допустимые символы")
        print("4. Запустить терминал")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            directory = input("Введите путь для создания корневой папки: ")
            create_root_folder(directory)
        elif choice == '2':
            directory = input("Введите путь к директории для генерации файлов и папок: ")
            generate_random_files_and_folders(directory)
        elif choice == '3':
            directory = input("Введите путь к директории для проверки: ")
            check_files_and_folders_in_directory(directory)
        elif choice == '4':
            open_terminal()
        elif choice == '5':
            print("Выход.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()
