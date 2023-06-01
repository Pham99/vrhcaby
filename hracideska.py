import itertools
from hracipole import HraciPole, Bar
from kamen import Kamen


class HraciDeska:

    def __init__(self) -> None:
        self.hracideska = [HraciPole() for _ in range(24)]
        self.hracideska.insert(0, Bar("cerny"))
        self.hracideska.append(Bar("bily"))
        self.bar_cerny = self.hracideska[0]
        self.bar_bily = self.hracideska[25]

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
    
    def display_mozne_tahy(self, hrac, kroky):
        smer = self.get_smer(hrac)

        tahy = {}
        for i, pole in enumerate(self.hracideska):
            if pole == None:
                continue
            elif pole.peek() == hrac.barva:
                tahy[i] = []
        if 0 in tahy.keys():
            tahy = {0: []}
        elif 25 in tahy.keys():
            tahy = {25: []}

        keys = list(tahy.keys()).copy()
        for start in keys:
            for vzdalenost in kroky:
                destinace = start + vzdalenost * smer
                if hrac.muzu_vyvest(self.hracideska) and start == hrac.nejvzdalenejsi_kamen(tahy.keys()):
                    destinace = self.clamp(destinace)
                if destinace >= self.left_border and destinace <= self.right_border:
                    if self.hracideska[destinace].peek() == hrac.barva or self.hracideska[destinace].length() < 2:
                        tahy[start].append(destinace)
            if tahy[start] == []:
                tahy.pop(start, None)
        return tahy
    
    def move_kamen(self, hrac, zacatek, konec):
        if self.hracideska[konec].peek() == hrac.barva or self.hracideska[konec].peek() == "neutral":
            self.hracideska[konec].push(self.hracideska[zacatek].pop())
        else:
            if hrac.barva == "cerny":
                self.bar_bily.push(self.hracideska[konec].pop())
            else:
                self.bar_cerny.push(self.hracideska[konec].pop())
            self.hracideska[konec].push(self.hracideska[zacatek].pop())

    def tah(self, zacatek, konec, kostka, hrac):
        smer = self.get_smer(hrac)
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
    
    def check(self, hrac):
        if hrac.barva == "cerny":
            if hrac.muzu_vyvest(self.hracideska):
                print(hrac.barva + " muze vyvadet kameny")
                self.right_border = 25
                return
            self.right_border = 24
            self.left_border = 1
            return
        else:
            if hrac.muzu_vyvest(self.hracideska):
                print(hrac.barva + " muze vyvadet kameny")
                self.left_border = 0
                return
            self.right_border = 24
            self.left_border = 1
            return
        
    def better_render(self):
        print("  1 1 1")
        print("  2 1 0 9 8 7   6 5 4 3 2 1")
        print("╔═════════════╤═════════════╦══╗")
        start = 12
        end = 0
        step = 1
        start2 = 0
        end2 = 5
        border = 6
        bar = self.bar_cerny
        for j in range(2):
            for i in range(start2, end2, step):
                print("║ ", end="")
                for index in range(start, end, -step):
                    if index == border:
                        print("│", end=" ")
                    if self.hracideska[index].length() > i:
                        print(self.hracideska[index], end=" ")
                    else:
                        print("∙", end=" ")
                if i == 0:
                    print("║" + str(bar).rjust(2, " ") + "║")
                else:
                    print("║  ║")
            if j == 0:
                print("║             │             ╠══╣")
            start = 13
            end = 25
            step = -1
            start2 = 4
            end2 = -1
            border = 19
            bar = self.bar_bily
        print("╚═════════════╧═════════════╩══╝")
        print("  1 1 1 1 1 1   1 2 2 2 2 2")
        print("  3 4 5 6 7 8   9 0 1 2 3 4")
        print("bar_bily: " + self.bar_bily.print_pole())
        print("bar_cerny: " + self.bar_cerny.print_pole() + "\n")

    def gameover_check(self):
        return self.bar_cerny.cil_length() >= 15 or self.bar_bily.cil_length() >= 15
    
    def eval_winner(self):
        if self.bar_cerny.cil_length() >= self.pocet_kamenu_na_vyhru:
            print("vyhral bily")
        else:
            print("vyhral cerny")

    def get_smer(self, hrac):
        if hrac.barva == "cerny":
            return 1
        else:
            return -1
        
    def clamp(self, value):
        if value > 25:
            return 25
        elif value < 0:
            return 0
        else:
            return value