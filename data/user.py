class User:
    def __init__(self, id: int, fullname: str, login: str, password:str , pincode: int):
        self.id = id
        self.fullname = fullname
        self.login = login
        self.password = password
        self.pincode = pincode

    @staticmethod
    def parse(row: tuple[str, str, str, str, str]):
        return User(int(row[0]), row[1], row[2], row[3], int(row[4]))
