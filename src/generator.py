class Generator:
    def __init__(self, be: bool):
        self.big_endian = be

    actor: bool = False
    revival: list = [1, 1]
    directory: str = "Enemized"
    big_endian: bool
