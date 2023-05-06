from kostka import Kostka
from kamen import Kamen
from hrac import Hrac, Hrac_CPU
from hracipole import HraciPole
from prettydice import Pretty_dice
import os
import itertools

class Vrhcaby:

    def __init__(self) -> None:
        self.hrac1 = None
        self.hrac2 = None
        self.currentplayer = None
        self.kostka = Kostka(6)
        self.hracideska = [HraciPole() for _ in range(26)]
        self.cil_bily = []
        self.cil_cerny = []
        self.bar_cerny = self.hracideska[0]
        self.bar_bily = self.hracideska[25]
        self.gameover = False

    def dvojkostka(self):
        kostka1 = self.kostka.hod_kostkou()
        kostka2 = self.kostka.hod_kostkou()
        if kostka1 == kostka2:
            return [kostka1]*4
        else:
            return [kostka1, kostka2]
        
    def moznosti(self):
        print("Vyberte barvu\n1: Cerny\n2: Bily")
        vyber1 = vyber_mezi_2()
        if vyber1 == 1:
            colour1 = "cerny"
            colour2 = "bily"
        else:
            colour1 = "bily"
            colour2 = "cerny"
        print("Vyberte soupere\n1: Hrac\n2: Pocitac (nefunguje)")
        vyber2 = vyber_mezi_2()
        if vyber2 == 1:
            self.hrac1 = Hrac(colour1)
            self.hrac2 = Hrac(colour2)
        else:
            self.hrac1 = Hrac(colour1)
            self.hrac2 = Hrac(colour2)

    def who_goes_first(self):
        while True:
            n1 = self.kostka.hod_kostkou()
            n2 = self.kostka.hod_kostkou()
            if  n1 == n2:
                print("same numbers")
                continue
            else:
                break
        if n1 > n2:
            self.currentplayer = self.hrac1
            print("jdes prvni")
        else:
            self.currentplayer = self.hrac2
            print("jdes druhy")

    def napln_desku(self):
        for _ in range(2):
            self.hracideska[1].push(Kamen("cerny"))
        for _ in range(5):
            self.hracideska[12].push(Kamen("cerny"))
        for _ in range(3):
            self.hracideska[17].push(Kamen("cerny"))
        for _ in range(5):
            self.hracideska[19].push(Kamen("cerny"))

        for _ in range(2):
            self.hracideska[24].push(Kamen("bily"))
        for _ in range(5):
            self.hracideska[13].push(Kamen("bily"))
        for _ in range(3):
            self.hracideska[8].push(Kamen("bily"))
        for _ in range(5):
            self.hracideska[6].push(Kamen("bily"))

    def napln_desku_debug(self):
        self.hracideska[1].push(Kamen("cerny"))
        self.hracideska[3].push(Kamen("bily"))
        self.hracideska[5].push(Kamen("bily"))
        self.hracideska[7].push(Kamen("bily"))
        self.hracideska[9].push(Kamen("bily"))


    def move_kamen(self, zacatek, konec):
        if self.hracideska[konec].peek() == self.currentplayer.barva or self.hracideska[konec].peek() == "neutral":
            self.hracideska[konec].push(self.hracideska[zacatek].pop())
        else:
            if self.currentplayer.barva == "cerny":
                self.bar_bily.push(self.hracideska[konec].pop())
            else:
                self.bar_cerny.push(self.hracideska[konec].pop())
            self.hracideska[konec].push(self.hracideska[zacatek].pop())
        # if self.hracideska[konec].length() < 2 and self.hracideska[konec].peek() != self.currentplayer.barva and self.hracideska[konec].peek() != "neutral":
        #     self.bar_bily.push(self.hracideska[konec].pop())
        # self.hracideska[konec].push(self.hracideska[zacatek].pop())

    def display_mozne_tahy(self, kroky):
        smer = self.get_smer()
        tahy = {}
        for i, pole in enumerate(self.hracideska):
            if pole == None:
                continue
            elif pole.peek() == self.currentplayer.barva:
                tahy[i] = []
        if 0 in tahy.keys():
            tahy = {0: []}
        elif 25 in tahy.keys():
            tahy = {25: []}
            
        keys = list(tahy.keys()).copy()
        for key in keys:
            for i in kroky:
                destinace = key + i * smer
                if destinace <= 24 and destinace >= 1:
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
    
    def tah(self, zacatek, konec, kostka):
        smer = self.get_smer()
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
    
    def render(self):
        print("\ncil bily:" + str(self.cil_bily))
        print("----------")
        for i, pole in enumerate(list(map(str,self.hracideska[1:-1]))):
            print(f"{i + 1} " + str(pole))
            if (i + 1) % 6 == 0:
                print("----------")
        print("cil cerny:" + str(self.cil_cerny))
        print("bar_bily: " + str(self.bar_bily))
        print("bar_cerny: " + str(self.bar_cerny) + "\n")

    def switch_players(self):
        if self.currentplayer == self.hrac1:
            self.currentplayer = self.hrac2
        else:
            self.currentplayer = self.hrac1

    def get_smer(self):
        if self.currentplayer.barva == "cerny":
            return 1
        else:
            return -1
    
    def play(self):
        self.moznosti()
        self.who_goes_first()
        self.napln_desku()
        while not self.gameover:
            #kostky = [2,2,2,2]
            kostky = self.dvojkostka()
            while len(kostky) > 0 and kostky != None:
                self.render()
                print(f"hraje: {self.currentplayer}")
                Pretty_dice.print_dice(kostky)
                print(f"vase kostky: " + str(kostky))
                mozne_tahy = self.display_mozne_tahy(self.vypocti_mozne_kroky(kostky))
                if mozne_tahy == {}:
                    print("zadne mozne tahy")
                    os.system("cls")
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
        
def vyber_mezi_2():
    while True:
        vyber = int(input("\nZadejte 1 nebo 2: "))
        if vyber == 1 or vyber == 2:
            return vyber
        else:
            print("zadali jste neco spatne")
            continue

def main():
    print("""
    :::     ::: :::::::::  :::    :::  ::::::::      :::     :::::::::  :::   ::: 
    :+:     :+: :+:    :+: :+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:   :+: 
    +:+     +:+ +:+    +:+ +:+    +:+ +:+         +:+   +:+  +:+    +:+  +:+ +:+  
    +#+     +:+ +#++:++#:  +#++:++#++ +#+        +#++:++#++: +#++:++#+    +#++:   
     +#+   +#+  +#+    +#+ +#+    +#+ +#+        +#+     +#+ +#+    +#+    +#+    
      #+#+#+#   #+#    #+# #+#    #+# #+#    #+# #+#     #+# #+#    #+#    #+#    
        ###     ###    ### ###    ###  ########  ###     ### #########     ###    
    """)

    print("1: PLAY\n2: QUIT")
    vyber = vyber_mezi_2()
    if vyber == 1:
        os.system("cls")
        a = Vrhcaby()
        a.play()
    else:
        quit()

if __name__ == "__main__":
    main()