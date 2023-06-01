from kostka import Kostka
from kamen import Kamen
from hrac import Hrac, Hrac_CPU
from hracipole import HraciPole, Bar
from prettydice import Pretty_dice
from hracideska import HraciDeska
import os
import itertools

class Vrhcaby:

    def __init__(self) -> None:
        self.hrac1 = None
        self.hrac2 = None
        self.currentplayer = None
        self.hracideska = HraciDeska()
        self.kostka = Kostka(6)
        self.left_border = 1
        self.right_border = 24
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
            print("Jdes prvni")
            input("press enter to continue:")
            os.system("cls")
            return self.hrac1
        else:
            print("Jdes druhy")
            input("press enter to continue:")
            os.system("cls")
            return self.hrac2

    def switch_players(self, hrac):
        if hrac == self.hrac1:
            return self.hrac2
        else:
            return self.hrac1
    
    def play(self):
        self.moznosti()
        self.tutorial()
        current_player = self.who_goes_first()
        self.hracideska.napln_desku()
        while not self.gameover:
            #kostky = [2,2,2,2]
            kostky = self.dvojkostka()
            while len(kostky) > 0 and kostky != None:
                self.hracideska.better_render()
                print(f"---- Hraje: {current_player.barva} ----")
                self.hracideska.check(current_player)
                Pretty_dice.print_dice(kostky)
                print(f"Vase kostky: " + str(kostky))
                mozne_tahy = self.hracideska.display_mozne_tahy(current_player ,self.hracideska.vypocti_mozne_kroky(kostky))
                if mozne_tahy == {}:
                    print("Zadne mozne tahy")
                    input("press enter to continue")
                    os.system("cls")
                    break
                print(f"Mozne tahy: {mozne_tahy}")
                vyber = current_player.play(mozne_tahy)
                if vyber[0] not in mozne_tahy.keys() or vyber[1] not in mozne_tahy[vyber[0]]:
                    print("zadal jste spatne")
                    continue
                kostky = self.hracideska.tah(vyber[0], vyber[1], kostky, current_player)
                input("press enter to continue")
                os.system("cls")
            current_player = self.switch_players(current_player)
            self.gameover = self.hracideska.gameover_check()
        self.hracideska.eval_winner()
        self.hracideska.better_render()
        input("press enter to continue:")
                 
    def tutorial(self):
        print("\nTUTORIAL:")
        print("dostanete takhle slovnik, jako seznam vsech moznych tahu:")
        example = {1: [3, 6, 8], 7: [9, 12, 14]}
        print(f"Mozne tahy: {example}")
        print("kde klice jsou pozice kamenu a prvky v listu jsou mista kam je muzete dat")
        print("zadejte ve tvaru klic mezera prvek v listu")
        print("napr. (1 8) nebo (7 12) bez zavorek")
        input("press enter to continue")
        
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