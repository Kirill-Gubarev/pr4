from PySide6.QtWidgets import (
	QMainWindow,
	QPushButton,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox
)
from PySide6.QtGui import QDoubleValidator
from data.payment import Payment
from datetime import datetime

class InsertWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("insert")
        self.__app = app
        self.__interfaceInit()

    def __interfaceInit(self):
        self.__mainLayoutInit()
        self.__categoryLayoutInit()
        self.__nameLayoutInit()
        self.__quantityLayoutInit()
        self.__priceLayoutInit()
        self.__buttonsLayoutInit()

    def __mainLayoutInit(self):
        self.__centralWidget = QWidget()
        self.setCentralWidget(self.__centralWidget)
        self.__mainLayout = QVBoxLayout()
        self.__centralWidget.setLayout(self.__mainLayout)

    def __categoryLayoutInit(self):
        self.__categoryLayout = QHBoxLayout()
        self.__mainLayout.addLayout(self.__categoryLayout)

        self.__categoryLabel = QLabel("category:")
        self.__categoryLayout.addWidget(self.__categoryLabel)

        self.__categoryComboBox = QComboBox()
        self.__categoryComboBox.blockSignals(True)

        categories = self.__app.db.getPaymentCategories();
        for category in categories:
            self.__categoryComboBox.addItem(category.name, category)

        self.__categoryComboBox.blockSignals(False)
        self.__categoryLayout.addWidget(self.__categoryComboBox)

    def __nameLayoutInit(self):
        self.__nameLayout = QHBoxLayout()
        self.__mainLayout.addLayout(self.__nameLayout)

        self.__nameLabel = QLabel("name:")
        self.__nameLayout.addWidget(self.__nameLabel)

        self.__nameLineEdit = QLineEdit()
        self.__nameLayout.addWidget(self.__nameLineEdit)

    def __quantityLayoutInit(self):
        self.__quantityLayout = QHBoxLayout()
        self.__mainLayout.addLayout(self.__quantityLayout)

        self.__quantityLabel = QLabel("quantity:")
        self.__quantityLayout.addWidget(self.__quantityLabel)

        self.__quantitySpinBox = QSpinBox()
        self.__quantitySpinBox.setMaximum(2**31-1)
        self.__quantityLayout.addWidget(self.__quantitySpinBox)

    def __priceLayoutInit(self):
        self.__priceLayout = QHBoxLayout()
        self.__mainLayout.addLayout(self.__priceLayout)

        self.__priceLabel = QLabel("price:")
        self.__priceLayout.addWidget(self.__priceLabel)

        self.__priceLineEdit = QLineEdit()
        validator = QDoubleValidator(0.0, 1e10, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.__priceLineEdit.setValidator(validator)
        self.__priceLayout.addWidget(self.__priceLineEdit)

        self.__currencyLabel = QLabel("р.")
        self.__priceLayout.addWidget(self.__currencyLabel)

    def __buttonsLayoutInit(self):
        self.__buttonsLayout = QHBoxLayout()
        self.__mainLayout.addLayout(self.__buttonsLayout)

        self.__addButton = QPushButton("add", clicked=self.__addPayment)
        self.__buttonsLayout.addWidget(self.__addButton)

        self.__cancelButton = QPushButton("cancel", clicked=lambda: self.hide())
        self.__buttonsLayout.addWidget(self.__cancelButton)

    def hide(self):
        self.__clearCurrentData()
        super().hide()

    def __clearCurrentData(self):
        self.__categoryComboBox.blockSignals(True)
        self.__categoryComboBox.setCurrentIndex(-1)
        self.__categoryComboBox.blockSignals(False)
        self.__nameLineEdit.clear()
        self.__quantitySpinBox.clear()
        self.__priceLineEdit.clear()

    def __addPayment(self):
        self.__app.db.addPayment(Payment(-1, datetime.now().date(),
                                self.__categoryComboBox.currentData().id,
                                self.__nameLineEdit.text(),
                                self.__quantitySpinBox.value(),
                                self.__priceLineEdit.text(),
                                self.__app.currentUser.id));
        self.hide()
