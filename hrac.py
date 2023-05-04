class Hrac:

    def __init__(self, barva) -> None:
        self.barva = barva

    def Play(self):
        vyber = input("zadejte prikaz: ").split(" ")
        return list(map(int, vyber))
    
    def __str__(self) -> str:
        return self.barva

class Hrac_CPU(Hrac):

    def __init__(self, barva) -> None:
        super.__init__(barva)

    def Play(self):
        print("beep boop")