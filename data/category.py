class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @staticmethod
    def parse(row: tuple[str, str]):
        return Category(int(row[0]), row[1])
