import random
import itertools

class Kostka:
    def __init__(self, pocet_hran) -> None:
        self.pocet_hran = pocet_hran

    def hod_kostkou(self):
        return random.randint(1,6)

class HraciPole:

    def __init__(self) -> None:
        self.__seznam = list()

    def push(self, value):
        self.__seznam.append(value)

    def pop(self):
        if len(self.__seznam) == 0:
            print("i cannot")
        else:
            return self.__seznam.pop()
        
    def peek(self):
        if len(self.__seznam) > 0:
            return self.__seznam[-1].get_barva()
        else:
            return None
        
    def length(self):
        return len(self.__seznam)
        
    def __str__(self) -> str:
        return str(list(map(str,self.__seznam))).replace("cerny", "o").replace("bily", "●")
    
class Vrhcaby:

    def __init__(self) -> None:
        self.hrac1 = Hrac()
        self.hrac2 = Hrac()
        self.kostka = Kostka()
        self.hracideska = [HraciPole() for i in range(24)]
        self.cil_bily = []
        self.cil_cerny = []
        self.bar_cerny = HraciPole()
        self.bar_bily = HraciPole()
        self.gameover = False

    def dvojkostka(self):
        kostka1 = self.kostka.hod_kostkou()
        kostka2 = self.kostka.hod_kostkou()
        if kostka1 == kostka2:
            return [kostka1]*4
        else:
            return [kostka1, kostka2]
    
    def napln_desku(self):
        for _ in range(2):
            self.hracideska[0].push(Kamen("cerny"))
        for _ in range(5):
            self.hracideska[11].push(Kamen("cerny"))
        for _ in range(3):
            self.hracideska[16].push(Kamen("cerny"))
        for _ in range(5):
            self.hracideska[18].push(Kamen("cerny"))

        for _ in range(2):
            self.hracideska[23].push(Kamen("bily"))
        for _ in range(5):
            self.hracideska[12].push(Kamen("bily"))
        for _ in range(3):
            self.hracideska[7].push(Kamen("bily"))
        for _ in range(5):
            self.hracideska[5].push(Kamen("bily"))

    def move_kamen(self, zacatek, konec):
        self.hracideska[konec].push(self.hracideska[zacatek].pop())

    def display_mozne_tahy(self, kroky):
        tahy = {}
        for i, pole in enumerate(self.hracideska):
            if pole == None:
                continue
            elif pole.peek() == "cerny":
                tahy[i] = []
        for key in tahy.keys():
            for i in kroky:
                destinace = key + i
                if destinace < 23 and destinace > -1:
                    if self.hracideska[destinace].peek() != "bily" and self.hracideska[destinace].length() < 2:
                        tahy[key].append(key + i)
        return tahy

    def vypocti_mozne_kroky(self, kroky):
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
    
    def render(self):
        print("\ncil bily:" + str(self.cil_bily))
        print("----------")
        for i, pole in enumerate(list(map(str,self.hracideska))):
            print(f"{i} " + str(pole))
            if (i + 1) % 6 == 0:
                print("----------")
        print("cil cerny:" + str(self.cil_cerny))
        print("bar_bily: " + str(self.bar_bily))
        print("bar_cerny: " + str(self.bar_cerny))

    def tah(self, zacatek, konec, dice):
     krok = konec - zacatek
     if krok in dice:
          self.move_kamen(zacatek, konec)
          dice.remove(krok)
     else:
        suma_dice = sum(dice)
        while suma_dice - krok != sum(dice):
             temp = dice.pop()
             self.move_kamen(zacatek, zacatek + temp)
             zacatek += temp
             dice.remove(krok)
        return dice

    def play(self):
        a = Vrhcaby()
        a.napln_desku()
        while not self.gameover:
            kolo = True
            if kolo:
                print("hraje cerny")
                kostky = a.dvojkostka()
                while len(kostky) > 0 and kostky != None:
                    print(f"dostali jste: " + str(kostky))
                    #if "cerny" in list(map(str, a.bar_cerny)): #needs work
                        #tah z baru od 0
                        #pass
                    #else:
                    print(a.display_mozne_tahy(a.vypocti_mozne_kroky(kostky)))
                    vyber = self.hrac1.Play()
                    a.move_kamen(int(vyber[0]), int(vyber[1]))
                    a.render()
                #kolo = False
                self.gameover_check()
        self.eval_winner()
                
    def eval_winner(self):
        if len(self.cil_bily) < 15:
            print("vyhral bily")
        else:
            print("vyhral cerny")

    def gameover_check(self):
        if len(self.cil_bily) > 14 or len(self.cil_cerny) > 14:
            self.gameover = True

class Kamen:

    def __init__(self, barva) -> None:
        self.barva = barva

    def get_barva(self):
        return self.barva

    def __str__(self) -> str:
        return str(self.barva)
    
class Hrac:

    def __init__(self) -> None:
        pass

    def Play(self):
        vyber = input("zadejte prikaz: ").split(" ")
        print("plaaay")
        return vyber

class Hrac_CPU():

    def __init__(self) -> None:
        pass

    def Play(self):
        print("beep boop")
        
a = Vrhcaby()
# a.napln_desku()
# a.render()
# dice = [4, 5]
# print(a.display_mozne_tahy(a.vypocti_mozne_kroky(dice)))
# dice = a.tah(0, 4, dice)
# a.render()
# print(dice)
a.play()


