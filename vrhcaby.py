import os
import random
import itertools

class Kostka:
    def __init__(self, pocet_hran) -> None:
        self.pocet_hran = pocet_hran

    def hod_kostkou(self):
        return random.randint(1, self.pocet_hran)

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
            return "neutral"
        
    def length(self):
        return len(self.__seznam)
        
    def __str__(self) -> str:
        if self.peek() == "cerny":
            symbol = "o"
        else:
            symbol = "●"
        return symbol * self.length()
        #return str(list(map(str,self.__seznam))).replace("cerny", "o").replace("bily", "●")
    
class Vrhcaby:

    def __init__(self) -> None:
        self.hrac1 = Hrac("cerny")
        self.hrac2 = Hrac("bily")
        self.currentplayer = self.hrac1
        self.kostka = Kostka(6)
        self.hracideska = [HraciPole() for _ in range(24)]
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

    def napln_desku_debug(self):
        self.hracideska[0].push(Kamen("cerny"))
        self.hracideska[2].push(Kamen("bily"))
        self.hracideska[4].push(Kamen("bily"))
        self.hracideska[6].push(Kamen("bily"))
        self.hracideska[8].push(Kamen("bily"))


    def move_kamen(self, zacatek, konec):
        if self.hracideska[konec].peek() == self.currentplayer.barva or self.hracideska[konec].peek() == "neutral":
            self.hracideska[konec].push(self.hracideska[zacatek].pop())
        else:
            if self.currentplayer.barva == "cerna":
                self.bar_bily.push(self.hracideska[konec].pop())
            else:
                self.bar_cerny.push(self.hracideska[konec].pop())
            self.hracideska[konec].push(self.hracideska[zacatek].pop())
        # if self.hracideska[konec].length() < 2 and self.hracideska[konec].peek() != self.currentplayer.barva and self.hracideska[konec].peek() != "neutral":
        #     self.bar_bily.push(self.hracideska[konec].pop())
        # self.hracideska[konec].push(self.hracideska[zacatek].pop())

    def display_mozne_tahy(self, kroky):
        if self.currentplayer.barva == "cerny":
            smer = 1
        else:
            smer = -1
        tahy = {}
        for i, pole in enumerate(self.hracideska):
            if pole == None:
                continue
            elif pole.peek() == self.currentplayer.barva:
                tahy[i] = []
        keys = list(tahy.keys()).copy()
        for key in keys:
            for i in kroky:
                destinace = key + i * smer
                if destinace < 24 and destinace > -1:
                    if self.hracideska[destinace].peek() == self.currentplayer.barva or self.hracideska[destinace].length() < 2:
                        tahy[key].append(destinace)
            if tahy[key] == []:
                tahy.pop(key, None)
        return tahy

    def vypocti_mozne_kroky(self, kostka):
        kroky = kostka.copy()
        if len(kroky) > 2:
            kroky = list(itertools.accumulate(kroky))
        elif len(kroky) == 2:
            kroky.append(kroky[0] + kroky[1])
        else:
            pass
        return kroky
    
    def render(self):
        print("\ncil bily:" + str(self.cil_bily))
        print("----------")
        for i, pole in enumerate(list(map(str,self.hracideska))):
            print(f"{i} " + str(pole))
            if (i + 1) % 6 == 0:
                print("----------")
        print("cil cerny:" + str(self.cil_cerny))
        print("bar_bily: " + str(self.bar_bily))
        print("bar_cerny: " + str(self.bar_cerny) + "\n")

    def tah(self, zacatek, konec, kostka):
        if self.currentplayer.barva == "cerny":
            smer = 1
        else:
            smer = -1
        krok = abs(konec - zacatek)
        if krok in kostka:
            self.move_kamen(zacatek, konec)
            kostka.remove(krok)
        else:
            suma_dice = sum(kostka)
            while suma_dice - krok != sum(kostka):
                temp = kostka.pop() * smer
                self.move_kamen(zacatek, zacatek + temp)
                zacatek += temp
        return kostka

    def switch_players(self):
        if self.currentplayer == self.hrac1:
            self.currentplayer = self.hrac2
        else:
            self.currentplayer = self.hrac1
    
    def play(self):
        self.napln_desku_debug()
        while not self.gameover:
            kostky = [2,2,2,2]
            #kostky = self.dvojkostka()
            while len(kostky) > 0 and kostky != None:
                self.render()
                print(f"hraje: {self.currentplayer}")
                print(f"vase kostky: " + str(kostky))
                #if "cerny" in list(map(str, a.bar_cerny)): #needs work
                    #tah z baru od 0
                    #pass
                #else:
                mozne_tahy = self.display_mozne_tahy(self.vypocti_mozne_kroky(kostky))
                if mozne_tahy == {}:
                    print("zadne mozne tahy")
                    break
                print(mozne_tahy)
                vyber = self.currentplayer.Play()
                if vyber[0] not in mozne_tahy.keys() or vyber[1] not in mozne_tahy[vyber[0]]:
                    print("zadal jste spatne")
                    continue
                kostky = self.tah(vyber[0], vyber[1], kostky)
                os.system("cls")
            self.switch_players()
            self.gameover_check()
        self.eval_winner()

    def test(self):
        print(self.currentplayer)
        print(self.currentplayer == "cerny")
                
    def eval_winner(self):
        if len(self.cil_bily) < 15:
            print("vyhral bily")
        else:
            print("vyhral cerny")

    def gameover_check(self):
        if len(self.cil_bily) > 14 or len(self.cil_cerny) > 14:
            self.gameover = True

    def __str__(self) -> str:
        return str(list(map(str,self.hracideska)))

class Kamen:

    def __init__(self, barva) -> None:
        self.barva = barva

    def get_barva(self):
        return self.barva

    def __str__(self) -> str:
        return str(self.barva)
    
class Hrac:

    def __init__(self, barva) -> None:
        self.barva = barva

    def Play(self):
        vyber = input("zadejte prikaz: ").split(" ")
        return list(map(int, vyber))
    
    def __str__(self) -> str:
        return self.barva

class Hrac_CPU(Hrac):

    def __init__(self) -> None:
        super.__init__()

    def Play(self):
        print("beep boop")
        
a = Vrhcaby()
a.play()
#a.test()

