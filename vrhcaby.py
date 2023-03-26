import random
import itertools

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
        
    def Peek(self):
        if len(self.seznam) > 0:
            return self.seznam[-1].Barva()
        else:
            return None
        
    def __str__(self) -> str:
        return str(list(map(str,self.seznam)))
    
class Vrhcaby:

    def __init__(self) -> None:
        self.hracideska = [Stack() for i in range(24)]
        self.cil_bily = []
        self.cil_cerny = []
        self.bar = []

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

    def Mozne_tahy(self, kroky):
        tahy = {}
        for i, pole in enumerate(self.hracideska):
            if pole == None:
                continue
            elif pole.Peek() == "cerny":
                tahy[i] = []
        for key in tahy.keys():
            for i in kroky:
                tahy[key].append(key + i)
        return tahy

    def Mozne_kroky(self, kroky):
        if len(kroky) > 2:
            kroky = list(itertools.accumulate(kroky))
            return kroky
        elif len(kroky) == 2:
            kroky.append(kroky[0] + kroky[1])
        else:
            return kroky
        return kroky

    def __str__(self) -> str:
        return str(list(map(str,self.hracideska)))
    
    def Render(self):
        print("\ncil bily:" + str(self.cil_bily))
        print("----------")
        for i, pole in enumerate(list(map(str,self.hracideska))):
            print(f"{i} " + str(pole))
            if (i + 1) % 6 == 0:
                print("----------")
        print("cil cerny:" + str(self.cil_cerny))
        print("bar: " + str(self.bar))

class Kamen:

    def __init__(self, barva) -> None:
        self.barva = barva

    def Barva(self):
        return self.barva

    def __str__(self) -> str:
        return str(self.barva)
        
a = Vrhcaby()
a.NaplnDesku()
while len(a.cil_bily) < 15 or len(a.cil_cerny < 15):
    kolo = True
    if kolo:
        print("hraje cerny")
        kostky = a.Dvojkostka()
        print(f"dostali jste: " + str(kostky))
        if "cerny" in list(map(str, a.bar)): #needs work
            #tah z baru od 0
            pass
        else:
            while len(kostky) > 0:
                print(a.Mozne_tahy(a.Mozne_kroky(kostky)))
                vyber = input("zadejte prikaz: ").split(" ")
                a.Test_Tah(vyber[0], vyber[1])
                a.Render()
                #fce that removes from kostky
        kolo = False
    else:
        print("hraje bily")
        kostky = a.Dvojkostka()
        print(f"dostali jste:" + str(kostky))
        if "bily" in list(map(str, a.bar)): #needs work
            #tah z baru od 0
            pass
        else:
            while len(kostky) > 0:
                print(a.Mozne_tahy(a.Mozne_kroky(kostky)))
                vyber = input("zadejte prikaz: ").split(" ")
                a.Test_Tah(vyber[0], vyber[1])
                a.Render()
                #fce that removes from kostky
        kolo = True
if len(a.cil_bily) < 15:
    print("vyhral bily")
else:
    print("vyhral cerny")

a.Render()
