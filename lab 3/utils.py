from tkinter import filedialog


def select_directory():
    directory = filedialog.askdirectory()
    if not directory:
        return None
    return directory
