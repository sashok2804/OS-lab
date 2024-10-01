import os

def list_drives():
    if os.name == 'nt':
        import string
        from ctypes import windll

        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter + ':\\')
            bitmask >>= 1
        return drives
    else:
        return ["/"]

def get_drive_choice():
    drives = list_drives()
    for i, drive in enumerate(drives):
        print(f"{i + 1}. {drive}")
    
    choice = int(input("Выберите диск: "))
    return drives[choice - 1]
