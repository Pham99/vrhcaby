import random

class Hrac:
    def __init__(self, barva) -> None:
        self.__barva = barva
        if self.__barva == "cerny":
            self.interval1 = 0
            self.interval2 = 19
        elif self.__barva == "bily":
            self.interval1 = 7
            self.interval2 = 26
        else:
            raise ValueError
        
    @property
    def barva(self):
        return self.__barva

    def play(self, mozne_tahy: dict) -> list:
        vyber = input("Zadejte prikaz: ").split(" ")
        return list(map(int, vyber))
    
    def muzu_vyvest(self, hraci_deska):
        for pole in hraci_deska[self.interval1:self.interval2]:
            if pole.peek() == self.__barva:
                return False
        return True
    
    def nejvzdalenejsi_kamen(self, keys) -> int:
        list(keys)
        if self.__barva == "cerny":
            return min(keys)
        else:
            return max(keys)


class Hrac_CPU(Hrac):
    def __init__(self, barva) -> None:
        super().__init__(barva)

    def play(self, mozne_tahy: dict) -> list:
        kamen = random.choice(list(mozne_tahy.keys()))
        kam = random.choice(mozne_tahy[kamen])
        print(f"CPU zvolil: {kamen} {kam}")
        return [kamen, kam]
    
