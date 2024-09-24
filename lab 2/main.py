import sys
from PyQt5.QtWidgets import QApplication, QTabWidget
from memory_app import MemoryApp
from terminal_app import CustomTerminal

class CombinedApp(QTabWidget):
    def __init__(self):
        super().__init__()

        self.memory_tab = MemoryApp()
        self.terminal_tab = CustomTerminal()

        self.addTab(self.memory_tab, "Чтение/Запись памяти")
        self.addTab(self.terminal_tab, "Терминал")

        self.setWindowTitle('Memory & Terminal App')

def main():
    app = QApplication(sys.argv)
    combined_app = CombinedApp()
    combined_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
