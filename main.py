import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('login.qss').read_text())
    window = LoginWindow()
    sys.exit(app.exec())
