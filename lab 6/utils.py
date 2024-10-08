from tkinter import filedialog

def select_directory():
    directory = filedialog.askdirectory(title="Выберите директорию")
    return directory if directory else None
