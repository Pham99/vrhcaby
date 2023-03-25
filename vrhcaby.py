import random

class Stack:

    def __init__(self) -> None:
        self.seznam = list()

    def Push(self, value):
        self.seznam.append(value)

    def Pop(self):
        if len(self.seznam) == 0:
            print("i cannot")
        else:
            return self.seznam.pop()
        
    def __str__(self) -> str:
        return str(list(map(str,self.seznam)))
    
class Vrhcaby:

    def __init__(self) -> None:
        self.hracideska = [Stack() for i in range(24)]

    def Dvojkostka(self):
        kostka1 = random.randint(1,6)
        kostka2 = random.randint(1,6)
        if kostka1 == kostka2:
            return [kostka1]*4
        else:
            return [kostka1, kostka2]
    
    def NaplnDesku(self):
        for _ in range(2):
            self.hracideska[0].Push(Kamen("cerny"))
        for _ in range(5):
            self.hracideska[11].Push(Kamen("cerny"))
        for _ in range(3):
            self.hracideska[16].Push(Kamen("cerny"))
        for _ in range(5):
            self.hracideska[18].Push(Kamen("cerny"))

        for _ in range(2):
            self.hracideska[23].Push(Kamen("bily"))
        for _ in range(5):
            self.hracideska[12].Push(Kamen("bily"))
        for _ in range(3):
            self.hracideska[7].Push(Kamen("bily"))
        for _ in range(5):
            self.hracideska[5].Push(Kamen("bily"))

    def Test_Tah(self, zacatek, konec):
        self.hracideska[konec].Push(self.hracideska[zacatek].Pop())


    def __str__(self) -> str:
        return str(list(map(str,self.hracideska)))
        
class Kamen:

    def __init__(self, barva) -> None:
        self.barva = barva

    def Barva(self):
        return self.barva

    def __str__(self) -> str:
        return str(self.barva)
        
a = Vrhcaby()
a.NaplnDesku()
print(a)
a.Test_Tah(0,2)
print(a)

