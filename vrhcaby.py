from kostka import Kostka
from kamen import Kamen
from hrac import Hrac, Hrac_CPU
from hracipole import HraciPole, Bar
from prettydice import Pretty_dice
import os
import itertools

class Vrhcaby:

    def __init__(self) -> None:
        self.hrac1 = None
        self.hrac2 = None
        self.currentplayer = None
        self.kostka = Kostka(6)
        self.hracideska = [HraciPole() for _ in range(24)]
        self.hracideska.insert(0, Bar("cerny"))
        self.hracideska.append(Bar("bily"))
        self.bar_cerny = self.hracideska[0]
        self.bar_bily = self.hracideska[25]
        self.left_border = 1
        self.right_border = 24
        self.pocet_kamenu_na_vyhru = 15
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
        print("\nVyberte soupere\n1: Hrac\n2: Pocitac\n3: Pocitac vs Pocitac")
        vyber2 = vyber_mezi_2()
        if vyber2 == 1:
            self.hrac1 = Hrac(colour1)
            self.hrac2 = Hrac(colour2)
        elif vyber2 == 2:
            self.hrac1 = Hrac(colour1)
            self.hrac2 = Hrac_CPU(colour2)
        else:
            self.hrac1 = Hrac_CPU(colour1)
            self.hrac2 = Hrac_CPU(colour2)

    def who_goes_first(self):
        while True:
            n1 = self.kostka.hod_kostkou()
            n2 = self.kostka.hod_kostkou()
            print("Hrac 1 dostal:")
            Pretty_dice.print_dice(n1)
            print("Hrac 2 dostal:")
            Pretty_dice.print_dice(n2)
            if  n1 == n2:
                print("Dostali jste stejna cisla, hodi se znovu.")
                continue
            else:
                break
        if n1 > n2:
            self.currentplayer = self.hrac1
            print("Jdes prvni")
        else:
            self.currentplayer = self.hrac2
            print("Jdes druhy")
        input("press enter to continue:")
        os.system("cls")

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
        self.hracideska[20].push(Kamen("cerny"))
        self.hracideska[19].push(Kamen("cerny"))
        self.hracideska[3].push(Kamen("bily"))
        self.hracideska[5].push(Kamen("bily"))
        self.hracideska[7].push(Kamen("bily"))
        self.hracideska[9].push(Kamen("bily"))

    def vypocti_mozne_kroky(self, kostka):
        kroky = kostka.copy()
        if len(kroky) > 2:
            kroky = list(itertools.accumulate(kroky))
        elif len(kroky) == 2:
            kroky.append(kroky[0] + kroky[1])
        else:
            pass
        return kroky

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
        for start in keys:
            for vzdalenost in kroky:
                destinace = start + vzdalenost * smer
                if self.currentplayer.muzu_vyvest(self.hracideska) and start == self.currentplayer.nejvzdalenejsi_kamen(tahy.keys()):
                    destinace = self.clamp(destinace)
                if destinace >= self.left_border and destinace <= self.right_border:
                    if self.hracideska[destinace].peek() == self.currentplayer.barva or self.hracideska[destinace].length() < 2:
                        tahy[start].append(destinace)
            if tahy[start] == []:
                tahy.pop(start, None)
        return tahy
    
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
                self.move_kamen(zacatek, self.clamp(zacatek + temp))
                zacatek += temp
                if zacatek > self.right_border or zacatek < self.left_border:
                    break
        return kostka
    
    def check(self):
        if self.currentplayer.barva == "cerny":
            if self.currentplayer.muzu_vyvest(self.hracideska):
                print(self.currentplayer.barva + " muze vyvadet kameny")
                self.right_border = 25
                return
            self.right_border = 24
            self.left_border = 1
            return
        else:
            if self.currentplayer.muzu_vyvest(self.hracideska):
                print(self.currentplayer.barva + " muze vyvadet kameny")
                self.left_border = 0
                return
            self.right_border = 24
            self.left_border = 1
            return

    def render(self):
        print("\n0 cil bily:" + self.bar_cerny.print_cil())
        print("----------")
        for i, pole in enumerate(list(map(str,self.hracideska[1:-1]))):
            print(f"{i + 1} " + str(pole))
            if (i + 1) % 6 == 0:
                print("----------")
        print("25 cil cerny:" + self.bar_bily.print_cil())
        print("----------")
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
        self.tutorial()
        self.who_goes_first()
        self.napln_desku()
        while not self.gameover:
            #kostky = [2,2,2,2]
            kostky = self.dvojkostka()
            while len(kostky) > 0 and kostky != None:
                self.render()
                print(f"---- Hraje: {self.currentplayer} ----")
                self.check()
                Pretty_dice.print_dice(kostky)
                print(f"Vase kostky: " + str(kostky))
                mozne_tahy = self.display_mozne_tahy(self.vypocti_mozne_kroky(kostky))
                if mozne_tahy == {}:
                    print("Zadne mozne tahy")
                    input("press enter to continue")
                    os.system("cls")
                    break
                print(f"Mozne tahy: {mozne_tahy}")
                vyber = self.currentplayer.play(mozne_tahy)
                if vyber[0] not in mozne_tahy.keys() or vyber[1] not in mozne_tahy[vyber[0]]:
                    print("zadal jste spatne")
                    continue
                kostky = self.tah(vyber[0], vyber[1], kostky)
                input("press enter to continue")
                os.system("cls")
            self.switch_players()
            self.gameover_check()
        self.eval_winner()
        self.render()
        input("press enter to continue:")
    
    def test(self):
        print(self.currentplayer)
        print(self.currentplayer == "cerny")
                
    def eval_winner(self):
        if self.bar_cerny.cil_length() >= self.pocet_kamenu_na_vyhru:
            print("vyhral bily")
        else:
            print("vyhral cerny")

    def gameover_check(self):
        if self.bar_cerny.cil_length() >= self.pocet_kamenu_na_vyhru or self.bar_bily.cil_length() >= self.pocet_kamenu_na_vyhru:
            self.gameover = True

    def clamp(self, value):
        if value > 25:
            return 25
        elif value < 0:
            return 0
        else:
            return value
        
    def tutorial(self):
        print("\nTUTORIAL:")
        print("dostanete takhle slovnik, jako seznam vsech moznych tahu:")
        example = {1: [3, 6, 8], 7: [9, 12, 14]}
        print(f"Mozne tahy: {example}")
        print("kde klice jsou pozice kamenu a prvky v listu jsou mista kam je muzete dat")
        print("zadejte ve tvaru klic mezera prvek v listu")
        print("napr. (1 8) nebo (7 12) bez zavorek")
        input("press enter to continue")

    def __str__(self) -> str:
        return str(list(map(str,self.hracideska)))
        
def vyber_mezi_2():
    while True:
        vyber = int(input("\nZadejte cislo: "))
        if vyber == 1 or vyber == 2 or vyber == 3:
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