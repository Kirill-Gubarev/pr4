from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,

    QComboBox,
    QPushButton,
    QLineEdit,
    QLabel
)
import bcrypt

class LoginWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("login")
        self.__app = app
        self.__currentUser = None
        self.__interfaceInit()

    def __interfaceInit(self):
        self.__mainLInit()
        self.__usernameLInit()
        self.__passwordLInit()
        self.__buttonsLInit()

    def __mainLInit(self):
        cw = QWidget()
        self.__mainL = QVBoxLayout()
        cw.setLayout(self.__mainL)
        self.setCentralWidget(cw)

    def __usernameLInit(self):
        self.__usernameL = QHBoxLayout()
        self.__usernameL.addWidget(QLabel("username"))

        self.__usernameCB = QComboBox(currentIndexChanged=self.__selectUser)
        for user in self.__app.db.getUsers():
            self.__usernameCB.addItem(user.login, user)

        self.__usernameL.addWidget(self.__usernameCB)
        self.__mainL.addLayout(self.__usernameL)

    def __passwordLInit(self):
        self.__passwordL = QHBoxLayout()
        self.__passwordL.addWidget(QLabel("password"))
        self.__passwordLE = QLineEdit(textChanged=lambda: self.__passwordLE.setStyleSheet(""))
        self.__passwordLE.setEchoMode(QLineEdit.Password)
        self.__passwordL.addWidget(self.__passwordLE)
        self.__mainL.addLayout(self.__passwordL)

    def __buttonsLInit(self):
        self.__buttonsL = QHBoxLayout()
        self.__buttonsL.addWidget(QPushButton("login", clicked=lambda: self.__login()))
        self.__buttonsL.addWidget(QPushButton("exit", clicked=lambda: exit()))
        self.__mainL.addLayout(self.__buttonsL)

    def __checkPassword(self, enteredPassword: str, truePassword: str):
        return bcrypt.checkpw(enteredPassword.encode("utf-8"), truePassword.encode("utf-8"))

    def __login(self):
        if self.__checkPassword(self.__passwordLE.text(), self.__currentUser.password):
            self.__app.currentUser = self.__currentUser
            self.__app.switchToMainWindow()
        else:
            self.__passwordLE.setStyleSheet("border: 1px solid red;")

    def __selectUser(self, index):
        self.__currentUser = self.__usernameCB.itemData(index)
