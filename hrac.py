import random

class Hrac:

    def __init__(self, barva) -> None:
        self.barva = barva
        if self.barva == "cerny":
            self.interval1 = 0
            self.interval2 = 19
        elif self.barva == "bily":
            self.interval1 = 7
            self.interval2 = 26
        else:
            raise ValueError

    def play(self, mozne_tahy):
        vyber = input("Zadejte prikaz: ").split(" ")
        return list(map(int, vyber))
    
    def muzu_vyvest(self, hraci_deska):
        for pole in hraci_deska[self.interval1:self.interval2]:
            if pole.peek() == self.barva:
                return False
        return True
    
    def nejvzdalenejsi_kamen(self, keys):
        list(keys)
        if self.barva == "cerny":
            return min(keys)
        else:
            return max(keys)

    def __str__(self) -> str:
        return self.barva

class Hrac_CPU(Hrac):

    def __init__(self, barva) -> None:
        super().__init__(barva)

    def play(self, mozne_tahy):
        kamen = random.choice(list(mozne_tahy.keys()))
        kam = random.choice(mozne_tahy[kamen])
        print(f"CPU zvolil: {kamen} {kam}")
        return [kamen, kam]
    
