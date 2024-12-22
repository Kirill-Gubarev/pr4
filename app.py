import sys
from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from login_window import LoginWindow
from insert_window import InsertWindow
from database import Database

class App:
    def __init__(self):
        self.db = Database().connect()
        self.currentUser = None

        self.__qApp = QApplication(sys.argv)
        self.__qApp.setStyleSheet("""
        QWidget {
            background-color: #1F1F1F;
            color: #ffffff;
        }
        """)

        self.__mainWindow = MainWindow(self)
        self.__loginWindow = LoginWindow(self)
        self.__insertWindow = InsertWindow(self)

        self.__currentWindow = self.__loginWindow

    def switchToMainWindow(self):
        self.__switchWindow(self.__mainWindow)

    def switchToInsertWindow(self):
        self.__switchWindow(self.__insertWindow)

    def __switchWindow(self, window):
        self.__currentWindow.hide()
        window.show()

    def __del__(self):
        self.db.close()

    def exec(self):
        self.__currentWindow.show()
        self.__qApp.exec()
        return self
