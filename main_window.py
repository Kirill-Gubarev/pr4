from PySide6.QtWidgets import (
    QApplication,

    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,

    QPushButton,
    QComboBox,
    QLabel,
    QFrame,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)
from PySide6.QtCore import QDate, Qt

from login_window import LoginWindow
from database import Database
from data.payment import Payment
from data.category import Category

from export_pdf import export_to_pdf

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("main")
        self.__app = app
        self.__categoriesCBChanged=False
        self.__categories = {}
        self.__payments = []
        self.__interfaceInit()

    def closeEvent(self, event):
        QApplication.quit()

    def __createItem(self, item: str):
        tableItem = QTableWidgetItem(item)
        tableItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return tableItem

    def __insertPayment(self, payment: Payment):
        row = self.__table.rowCount()
        self.__table.setRowCount(row + 1)
        self.__table.setItem(row, 0, self.__createItem(payment.name))
        self.__table.setItem(row, 1, self.__createItem(str(payment.quantity)))
        self.__table.setItem(row, 2, self.__createItem(str(payment.price)))
        self.__table.setItem(row, 3, self.__createItem(str(payment.price * payment.quantity)))
        self.__table.setItem(row, 4, self.__createItem(self.__categories[payment.category_id].name))

    def __dataIsMatchConditions(self, payment: Payment):
        dateFrom = self.__dateFrom.date().toPython()
        dateTo = self.__dateTo.date().toPython()
        return (
                (dateFrom <= payment.date and
                payment.date <= dateTo) and

                (self.__categoriesCB.currentData().id == payment.category_id or
                self.__categoriesCB.currentData().id == -1)
        )

    def __dataLoad(self):
        if self.__app.currentUser == None:
            return

        self.__categoriesLoad()
        self.__paymentsLoad()
        if not self.__categoriesCBChanged:
            self.__categoriesCBLoad()
        self.__categoriesCBChanged=False
        self.__tableLoad()

    def __categoriesLoad(self):
        data = self.__app.db.getPaymentCategories()
        for category in data:
            self.__categories[category.id] = category

    def __paymentsLoad(self):
        self.__payments = self.__app.db.getPayments(self.__app.currentUser.id)

    def __categoriesCBLoad(self):
        self.__categoriesCB.blockSignals(True)
        self.__categoriesCB.clear()
        self.__categoriesCB.addItem("None", Category(-1, "None"))
        for id in self.__categories:
            category = self.__categories[id]
            self.__categoriesCB.addItem(category.name, category)
        self.__categoriesCB.blockSignals(False)

    def __tableLoad(self):
        self.__table.clearContents()
        self.__table.setRowCount(0)

        for payment in self.__payments:
            if self.__dataIsMatchConditions(payment):
                self.__insertPayment(payment)

    def show(self):
        self.__dataLoad()
        super().show()

    def __interfaceInit(self):
        #main layout
        self.__centralWidget = QWidget()
        self.__mainL = QVBoxLayout()
        self.__centralWidget.setLayout(self.__mainL)
        self.setCentralWidget(self.__centralWidget)

        #top bar
        self.__topBarInit()

        #line
        self.__mainL.addWidget(self.__createLine(QFrame.HLine))

        #table
        self.__table = QTableWidget(0,5)
        self.__table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.__table.setHorizontalHeaderLabels(["name of payment", "quantity", "price", "sum", "category"])
        header = self.__table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.__mainL.addWidget(self.__table)


    def __topBarInit(self):
        self.__topBarL = QHBoxLayout()

        # + and - buttons
        self.__topBarL.addWidget(QPushButton("+", clicked=self.__app.switchToInsertWindow))
        self.__topBarL.addWidget(QPushButton("-", clicked=self.__deletePayment))

        #line
        self.__topBarL.addWidget(self.__createLine(QFrame.VLine))

        #date
        currentDate = QDate.currentDate()
        startOfMonthDate = QDate(2016, 11, 1)
        endOfMonthDate = QDate(2025, 1, 1)
        self.__topBarL.addWidget(QLabel("from"))
        self.__dateFrom = self.__createDateEdit(startOfMonthDate)
        self.__topBarL.addWidget(self.__dateFrom)
        self.__topBarL.addWidget(QLabel("to"))
        self.__dateTo = self.__createDateEdit(endOfMonthDate)
        self.__topBarL.addWidget(self.__dateTo)

        #category
        self.__topBarL.addWidget(QLabel("category:"))
        self.__categoriesCB = QComboBox(currentIndexChanged=self.__changeConditions)
        self.__topBarL.addWidget(self.__categoriesCB)

        #buttons
        self.__topBarL.addWidget(QPushButton("select", clicked=lambda: print("select")))
        self.__topBarL.addWidget(QPushButton("update", clicked=self.__dataLoad))
        self.__topBarL.addWidget(QPushButton("export", clicked=self.__export))

        self.__mainL.addLayout(self.__topBarL)

    def __export(self):
        export_to_pdf(self.__table, "export.pdf")

    def __deletePayment(self):
        index = self.__table.currentRow()

        if index >= 0:
            reply = QMessageBox.question(self, "Warning",
                                         "Are you sure you want to delete this row?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.__app.db.deletePayment(self.__payments[index].id)
                self.__dataLoad()

        else:
            QMessageBox.warning(self, "Error", "choose row to delete")


    def __changeConditions(self):
        self.__categoriesCBChanged=True
        self.__dataLoad()

    def __createDateEdit(self, date):
        dateEdit = QDateEdit(dateChanged=self.__changeConditions)
        dateEdit.blockSignals(True)
        dateEdit.setCalendarPopup(True)
        dateEdit.setDisplayFormat("dd.MM.yyyy")
        dateEdit.setDate(date)
        dateEdit.blockSignals(False)
        return dateEdit

    def __createLine(self, orientation):
        line = QFrame()
        line.setFrameShape(orientation)
        return line
