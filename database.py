import psycopg2, os, json

from data.user import User
from data.payment import Payment
from data.category import Category
import bcrypt

class Database:
    def __init__(self, configFile="db_config.json"):
        self.__config = self.__loadConfig(configFile)
        self.__connection = None

    def __loadConfig(self, configFile):
        if not os.path.exists(configFile):
            raise FileNotFoundError(f"file {configFile} not found.")
        with open(configFile, "r") as file:
            return json.load(file)

    def connect(self):
        if not self.__connection or self.connection.closed:
            try:
                self.__connection = psycopg2.connect(
                    dbname=self.__config["db_name"],
                    user=self.__config["user"],
                    password=self.__config["password"],
                    host=self.__config["host"],
                    port=self.__config["port"]
                )
            except psycopg2.Error as e:
                print(f"database connection error: {e}")
                raise
        return self

    def close(self):
        if self.__connection and not self.__connection.closed:
            self.__connection.close()
        return self

    def addPayment(self, payment):
        cur = self.__connection.cursor()
        values = (payment.date, payment.category_id, payment.name, payment.quantity, payment.price, payment.user_id)
        cur.execute("""
        INSERT INTO Payments (date, category_id, name, quantity, price, user_id) VALUES
        (%s, %s, %s, %s, %s, %s);
                    """, values)
        self.__connection.commit()

    def getUsers(self):
        cur = self.__connection.cursor()
        cur.execute("""
        SELECT *
        FROM users;
                    """)

        users = []
        for row in cur.fetchall():
            user = User.parse(row)
            users.append(user)
        cur.close()

        return users

    def getPayments(self, user_id: int):
        cur = self.__connection.cursor()
        cur.execute("""
        SELECT *
        FROM payments
        WHERE payments.user_id = %s;
                    """, (user_id,))

        payments = []
        for row in cur.fetchall():
            payment = Payment.parse(row)
            payments.append(payment)
        cur.close()

        return payments

    def getPaymentCategories(self):
        cur = self.__connection.cursor()
        cur.execute("""
        SELECT *
        FROM payment_categories;
                    """)
        categories = []
        for row in cur.fetchall():
            category = Category.parse(row)
            categories.append(category)
        cur.close()

        return categories

    def deletePayment(self, payment_id: int):
        cur = self.__connection.cursor()
        cur.execute("""
            DELETE FROM payments
            WHERE id = %s;
        """, (payment_id, ))
        cur.close()
        self.__connection.commit()
