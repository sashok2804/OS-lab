import tkinter as tk
from tkinter import ttk, messagebox
from folder_manager import create_root_folder, generate_random_files_and_folders
from file_checker import check_files_and_folders_in_directory
from terminal_launcher import run_terminal_command
from utils import select_directory
from auth import authenticate_user, authenticate_admin, is_admin, is_user

class Application(tk.Tk):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.title("File Manager GUI")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self)
        
        # Создаём вкладки
        tab_file_manager = ttk.Frame(tab_control)
        tab_control.add(tab_file_manager, text='File Manager')

        tab_terminal = ttk.Frame(tab_control)
        tab_control.add(tab_terminal, text='Terminal')
        
        # Настраиваем доступность вкладок в зависимости от роли
        if is_admin(self.role):
            self.create_file_manager_tab(tab_file_manager)
        elif is_user(self.role):
            self.create_user_limited_tab(tab_file_manager)

        self.create_terminal_tab(tab_terminal)
        
        tab_control.pack(expand=1, fill='both')

    def create_file_manager_tab(self, tab):
        ttk.Label(tab, text="Выберите действие").pack(pady=10)
        btn_create_folder = ttk.Button(tab, text="Создать корневую папку", command=self.create_folder)
        btn_create_folder.pack(pady=5)

        btn_generate_files = ttk.Button(tab, text="Генерация файлов и папок", command=self.generate_files)
        btn_generate_files.pack(pady=5)

        btn_check_files = ttk.Button(tab, text="Проверка символов в именах", command=self.check_files)
        btn_check_files.pack(pady=5)

    def create_user_limited_tab(self, tab):
        ttk.Label(tab, text="Выберите действие (Ограниченный доступ)").pack(pady=10)
        # Ограниченный функционал для User
        btn_check_files = ttk.Button(tab, text="Проверка символов в именах", command=self.check_files)
        btn_check_files.pack(pady=5)

    def create_terminal_tab(self, tab):
        ttk.Label(tab, text="Управление терминалом").pack(pady=10)
        
        self.terminal_output = tk.Text(tab, height=15, width=70, state='disabled')
        self.terminal_output.pack(pady=5)

        self.command_entry = ttk.Entry(tab, width=50)
        self.command_entry.pack(side=tk.LEFT, padx=5, pady=5)

        btn_run_command = ttk.Button(tab, text="Выполнить", command=self.run_terminal_command)
        btn_run_command.pack(side=tk.LEFT, padx=5, pady=5)

        self.command_entry.bind('<Return>', lambda event: self.run_terminal_command())
    
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
            if command.strip() == 'clear':
                self.clear_terminal()
            else:
                output = run_terminal_command(command)
                self.display_terminal_output(output)
            self.command_entry.delete(0, tk.END)

    def display_terminal_output(self, output):
        self.terminal_output.config(state='normal')
        self.terminal_output.insert(tk.END, f"$ {output}\n")
        self.terminal_output.config(state='disabled')
        self.terminal_output.see(tk.END)

    def clear_terminal(self):
        self.terminal_output.config(state='normal')
        self.terminal_output.delete(1.0, tk.END)
        self.terminal_output.config(state='disabled')

# Логика аутентификации пользователя при запуске программы
def login():
    login_window = tk.Tk()
    login_window.title("Login")
    
    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()
    
    tk.Label(login_window, text="Password (для User):").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()
    
    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if username == "Admin":
            # Попытка аутентификации Admin с сертификатом
            cert_path = tk.filedialog.askopenfilename(title="Выберите сертификат Admin")
            if authenticate_admin(cert_path):
                login_window.destroy()
                app = Application("Admin")
                app.mainloop()
            else:
                messagebox.showerror("Ошибка", "Неверный сертификат.")
        elif username == "User":
            # Базовая аутентификация для User
            if authenticate_user(username, password):
                login_window.destroy()
                app = Application("User")
                app.mainloop()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль.")
    
    btn_login = tk.Button(login_window, text="Войти", command=on_login)
    btn_login.pack()
    
    login_window.mainloop()

if __name__ == "__main__":
    login()
