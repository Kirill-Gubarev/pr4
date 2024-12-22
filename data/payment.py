from datetime import date

class Payment:
    def __init__(self, id: int,  date: date, category_id: int, name: str,
                 quantity: int, price: float, user_id: int):
        self.id = id
        self.date = date
        self.category_id = category_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.user_id = user_id

    @staticmethod
    def parse(row: tuple[str, str, str, str, str, str, str]):
        return Payment(int(row[0]), row[1], int(row[2]), row[3], int(row[4]), float(row[5]), int(row[6]))
