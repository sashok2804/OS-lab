import tkinter as tk
from tkinter import ttk, messagebox
from folder_manager import create_root_folder, generate_random_files_and_folders
from file_checker import check_files_and_folders_in_directory
from terminal_launcher import run_terminal_command
from utils import select_directory


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Manager GUI")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self)

        # Вкладка для управления файлами и папками
        tab_file_manager = ttk.Frame(tab_control)
        tab_control.add(tab_file_manager, text='File Manager')

        # Вкладка для терминала
        tab_terminal = ttk.Frame(tab_control)
        tab_control.add(tab_terminal, text='Terminal')

        tab_control.pack(expand=1, fill='both')

        # Компоненты для вкладки File Manager
        ttk.Label(tab_file_manager, text="Выберите действие").pack(pady=10)

        btn_create_folder = ttk.Button(tab_file_manager, text="Создать корневую папку", command=self.create_folder)
        btn_create_folder.pack(pady=5)

        btn_generate_files = ttk.Button(tab_file_manager, text="Генерация файлов и папок", command=self.generate_files)
        btn_generate_files.pack(pady=5)

        btn_check_files = ttk.Button(tab_file_manager, text="Проверка символов в именах", command=self.check_files)
        btn_check_files.pack(pady=5)

        # Компоненты для вкладки Terminal
        ttk.Label(tab_terminal, text="Управление терминалом").pack(pady=10)

        self.terminal_output = tk.Text(tab_terminal, height=15, width=70, state='disabled')
        self.terminal_output.pack(pady=5)

        self.command_entry = ttk.Entry(tab_terminal, width=50)
        self.command_entry.pack(side=tk.LEFT, padx=5, pady=5)

        btn_run_command = ttk.Button(tab_terminal, text="Выполнить", command=self.run_terminal_command)
        btn_run_command.pack(side=tk.LEFT, padx=5, pady=5)

    def create_folder(self):
        directory = select_directory()
        if directory:
            create_root_folder(directory)

    def generate_files(self):
        directory = select_directory()
        if directory:
            generate_random_files_and_folders(directory)

    def check_files(self):
        directory = select_directory()
        if directory:
            check_files_and_folders_in_directory(directory)

    def run_terminal_command(self):
        command = self.command_entry.get()
        if command:
            output = run_terminal_command(command)
            self.display_terminal_output(output)
            self.command_entry.delete(0, tk.END)

    def display_terminal_output(self, output):
        self.terminal_output.config(state='normal')
        self.terminal_output.insert(tk.END, f"$ {output}\n")
        self.terminal_output.config(state='disabled')
        self.terminal_output.see(tk.END)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
