from kostka import Kostka
from hrac import Hrac, Hrac_CPU
from prettydice import Pretty_dice
from hracideska import HraciDeska
from kamen import Kamen
import os
import json


class Vrhcaby:
    def __init__(self, hrac1=None, hrac2=None) -> None:
        self.hrac1 = hrac1
        self.hrac2 = hrac2
        self.hracideska = HraciDeska()
        self.kostka = Kostka(6)
        self.gameover = False
        self.pocet_kol = 0

    def dvojkostka(self) -> list:
        kostka1 = self.kostka.hod_kostkou()
        kostka2 = self.kostka.hod_kostkou()
        if kostka1 == kostka2:
            return [kostka1]*4
        else:
            return [kostka1, kostka2]
        
    def moznosti_menu(self) -> None:
        print("Vyberte barvu\n1: Cerny\n2: Bily")
        vyber1 = vyber_mezi_n_options(2)
        if vyber1 == 1:
            colour1 = "cerny"
            colour2 = "bily"
        else:
            colour1 = "bily"
            colour2 = "cerny"
        print("\nVyberte soupere\n1: Hrac\n2: Pocitac\n3: Pocitac vs Pocitac")
        vyber2 = vyber_mezi_n_options(3)
        if vyber2 == 1:
            self.hrac1 = Hrac(colour1)
            self.hrac2 = Hrac(colour2)
        elif vyber2 == 2:
            self.hrac1 = Hrac(colour1)
            self.hrac2 = Hrac_CPU(colour2)
        else:
            self.hrac1 = Hrac_CPU(colour1)
            self.hrac2 = Hrac_CPU(colour2)

    def set_turn_order(self) -> Hrac:
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

    def switch_players(self, hrac: Hrac) -> Hrac:
        if hrac == self.hrac1:
            return self.hrac2
        else:
            return self.hrac1    

    def message_pause_clear(self, message: str="") -> None:
        print(message)
        input("Press enter to continue")
        os.system("cls")
        
    def gameloop(self, kostky: list, current_player: Hrac) -> None:
        self.hracideska.render_hracipole()  
        print(f"---- Hraje: {current_player.barva} | {self.pocet_kol}. kolo ----")
        self.hracideska.check_vyvedeni(current_player)
        Pretty_dice.print_dice(kostky)
        print(f"Vase kostky: " + str(kostky))
        mozne_tahy = self.hracideska.get_mozne_tahy(current_player ,self.hracideska.vypocti_mozne_kroky(kostky))
        if mozne_tahy == {}:
            self.message_pause_clear("Žádné možné tahy :(")
            kostky.clear()
            return
        print(f"Mozne tahy: {mozne_tahy}")
        vyber = current_player.play(mozne_tahy)
        if isinstance(vyber, list):
            if vyber[0] not in mozne_tahy.keys() or vyber[1] not in mozne_tahy[vyber[0]]:
                self.message_pause_clear("Neplatný tah")
                return
        elif vyber == "exit":
            os.system("cls")
            main()
        elif vyber == "save":
            self.savegame(kostky, current_player)
            self.message_pause_clear("game saved")
            return
        else:
            self.message_pause_clear("Špatný vstup")
            return
        self.hracideska.tah(vyber[0], vyber[1], kostky, current_player)
        self.message_pause_clear()
    
    def newgame(self):
        self.moznosti_menu()
        self.tutorial()
        current_player = self.set_turn_order()
        self.hracideska.napln_desku()
        return current_player
    
    def loadsave(self, data):
        self.pocet_kol = data["vrhcaby"][2]
        for i in range(30):
            clr = data["kameny"][i]["barva"]
            position = data["kameny"][i]["historie_pozic"]
            kills = data["kameny"][i]["kill_count"]
            self.hracideska.kameny.append(Kamen(clr,position,kills))
        self.hracideska.napln_desku_from_save()
        if data["vrhcaby"][4]["_Hrac__barva"] == self.hrac1.barva:
            return self.hrac1
        else:
            return self.hrac2

    def play(self, new= True, savedata= None) -> None:
        if new == True:
            current_player = self.newgame()
        else:
            current_player = self.loadsave(savedata)
        while not self.gameover:
            kostky = self.dvojkostka()
            while len(kostky) > 0:
                self.gameloop(kostky, current_player)
            current_player = self.switch_players(current_player)
            self.gameover = self.hracideska.gameover_check()
            self.pocet_kol += 1
        self.hracideska.render_hracipole()
        self.hracideska.evaluate_winner(self.hrac1, self.hrac2)
        self.showstats()
        input("press enter to continue:")
        main()

    def savegame(self, kostky, current_player):
        list_kameny = []
        for kamen in self.hracideska.kameny:
            list_kameny.append(kamen.__dict__)
        save = {"kameny": list_kameny}
        tojson_vrhcabi = [self.hrac1.__dict__, self.hrac2.__dict__,self.pocet_kol, kostky, current_player.__dict__]
        save["vrhcaby"] = tojson_vrhcabi
        with open("savefile.json", "w") as rl:
            json.dump(save, rl, indent = 4)
                 
    def tutorial(self) -> None:
        print("\nTUTORIAL:")
        print("dostanete takhle slovnik, jako seznam vsech moznych tahu:")
        example = {1: [3, 6, 8], 7: [9, 12, 14]}
        print(f"Mozne tahy: {example}")
        print("kde klice jsou pozice kamenu a prvky v listu jsou mista kam je muzete dat")
        print("zadejte ve tvaru klic mezera prvek v listu")
        print("napr. (1 8) nebo (7 12) bez zavorek")
        print("taky muzete napsat save na ulozeni hry a exit na vraceni do hlavniho menu")
        input("press enter to continue")
        os.system("cls")
    
    def showstats(self):
        print(f"Počet odehraných kol: {self.pocet_kol}")
        self.hracideska.showstats()

        
def vyber_mezi_n_options(n: int) -> int:
    while True:
        vyber = input("\nZadejte cislo: ")
        if not vyber.isdecimal():
            print("Nezadali jste číslo")
            continue
        vyber = int(vyber)
        if vyber in list(range(1,n + 1)):
            return vyber
        else:
            print(f"Číslo je mimo rozsah od 1 do {n}")
            continue

def main():
    os.system("cls")
    print("""
    :::     ::: :::::::::  :::    :::  ::::::::      :::     :::::::::  :::   ::: 
    :+:     :+: :+:    :+: :+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:   :+: 
    +:+     +:+ +:+    +:+ +:+    +:+ +:+         +:+   +:+  +:+    +:+  +:+ +:+  
    +#+     +:+ +#++:++#:  +#++:++#++ +#+        +#++:++#++: +#++:++#+    +#++:   
     +#+   +#+  +#+    +#+ +#+    +#+ +#+        +#+     +#+ +#+    +#+    +#+    
      #+#+#+#   #+#    #+# #+#    #+# #+#    #+# #+#     #+# #+#    #+#    #+#    
        ###     ###    ### ###    ###  ########  ###     ### #########     ###    
    """)

    print("1: NEW GAME\n2: LOAD GAME\n3: QUIT")
    vyber = vyber_mezi_n_options(3)
    if vyber == 1:
        os.system("cls")
        a = Vrhcaby()
        a.play()
    if vyber == 2:
        os.system("cls")
        with open("savefile.json", "r") as j:
            data = json.load(j)
        if data["vrhcaby"][0]["isahuman"] == True:
            hrac1 = Hrac(data["vrhcaby"][0]["_Hrac__barva"])
        else:
            hrac1 = Hrac_CPU(data["vrhcaby"][0]["_Hrac__barva"])
        if data["vrhcaby"][1]["isahuman"] == True:
            hrac2 = Hrac(data["vrhcaby"][1]["_Hrac__barva"])
        else:
            hrac2 = Hrac_CPU(data["vrhcaby"][1]["_Hrac__barva"])
        a = Vrhcaby(hrac1, hrac2)
        a.play(False, data)
    else:
        quit()

if __name__ == "__main__":
    main()