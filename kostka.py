import random

class Kostka:
    def __init__(self, pocet_hran) -> None:
        self.pocet_hran = pocet_hran

    def hod_kostkou(self):
        return random.randint(1, self.pocet_hran)
