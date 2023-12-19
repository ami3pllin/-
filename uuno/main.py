#main.py

import sys
import locale
from PyQt6.QtWidgets import QApplication
from windows import UserTypeWindow
import sys

def excepthook(type, value, traceback):
    print("Unhandled exception:", type, value)
    sys.__excepthook__(type, value, traceback)

sys.excepthook = excepthook

# Установка кодировки для корректного отображения в консоли Windows
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1)

# Установка предпочтительной кодировки
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UserTypeWindow()
    ex.show()
    sys.exit(app.exec())
