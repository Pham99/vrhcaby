import itertools
from hracipole import HraciPole, Bar
from kamen import Kamen


class HraciDeska:

    def __init__(self) -> None:
        self.hracideska = [HraciPole() for _ in range(24)]
        self.hracideska.insert(0, Bar("cerny"))
        self.hracideska.append(Bar("bily"))
        self.bar_cerny_cil_bily = self.hracideska[0]
        self.bar_bily_cil_cerny = self.hracideska[25]
        self.left_border = 1
        self.right_border = 24

    def napln_desku(self) -> None:
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

    def vypocti_mozne_kroky(self, kostka: list) -> list:
        kroky = kostka.copy()
        if len(kroky) > 2:
            kroky = list(itertools.accumulate(kroky))
        elif len(kroky) == 2:
            kroky.append(kroky[0] + kroky[1])
        else:
            pass
        return kroky
    
    def get_mozne_tahy(self, hrac, kroky: list) -> dict:
        smer = self.get_smer(hrac)
        # klice jsou pozice odkud se da tahnout
        tahy = {}
        for i, pole in enumerate(self.hracideska):
            if pole == None:
                continue
            elif pole.peek() == hrac.barva:
                tahy[i] = []
        # jestli je neco v baru tak muze tahnout jen z baru
        if 0 in tahy.keys():
            tahy = {0: []}
        elif 25 in tahy.keys():
            tahy = {25: []}
        # do klicu se pridaji listi s moznymi tahy
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
    
    def move_kamen(self, hrac, zacatek: int, konec: int) -> None:
        if self.hracideska[konec].peek() == hrac.barva or self.hracideska[konec].peek() == "neutral":
            self.hracideska[konec].push(self.hracideska[zacatek].pop())
        else:
            if hrac.barva == "cerny":
                self.bar_bily_cil_cerny.push(self.hracideska[konec].pop())
            else:
                self.bar_cerny_cil_bily.push(self.hracideska[konec].pop())
            self.hracideska[konec].push(self.hracideska[zacatek].pop())

    def tah(self, zacatek: int, konec: int, kostka: list, hrac) -> list:
        smer = self.get_smer(hrac)
        krok = abs(konec - zacatek)
        if krok in kostka:
            self.move_kamen(hrac, zacatek, konec)
            kostka.remove(krok)
        else:
            suma_dice = sum(kostka)
            while suma_dice - krok != sum(kostka):
                temp = kostka.pop() * smer
                self.move_kamen(hrac, zacatek ,self.clamp(zacatek + temp))
                zacatek += temp
                if zacatek > self.right_border or zacatek < self.left_border:
                    break
        return kostka
    
    def get_tallest_pole(self, start, end) -> int:
        biggest = 0
        for i in range(start, end + 1):
            if self.hracideska[i].length() > biggest:
                biggest = self.hracideska[i].length()
        return biggest
    
    def check_vyvedeni(self, hrac) -> None:
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
        
    def render_hracipole(self) -> None:
        print(" 12 11 10  9  8  7     6  5  4  3  2  1")
        print("╔═══════════════════╤════════════════════╦══╗")
        vertical_scan = range(0, self.clamp(self.get_tallest_pole(1, 12), 5))
        horizontal_scan = range(12, 0, -1)
        border = 6
        bar = self.bar_cerny_cil_bily
        for j in range(2):
            for i in vertical_scan:
                print("║ ", end="")
                for index in horizontal_scan:
                    if index == border:
                        print("│", end="  ")
                    if self.hracideska[index].length() > i:
                        print(self.hracideska[index], end="  ")
                    else:
                        print("∙", end="  ")
                if i == 0:
                    print("║" + str(bar).rjust(2, " ") + "║")
                else:
                    print("║  ║")
            if j == 0:
                print("║                   │                    ╠══╣")
            vertical_scan = reversed(range(0 ,self.clamp(self.get_tallest_pole(13, 24), 5)))
            horizontal_scan = range(13, 25)
            border = 19
            bar = self.bar_bily_cil_cerny
        print("╚═══════════════════╧════════════════════╩══╝")
        print(" 13 14 15 16 17 18    19 20 21 22 23 24")
        print("bar_bily: " + self.bar_bily_cil_cerny.print_pole())
        print("bar_cerny: " + self.bar_cerny_cil_bily.print_pole() + "\n")

    def gameover_check(self) -> bool:
        return self.bar_cerny_cil_bily.cil_length() >= 15 or self.bar_bily_cil_cerny.cil_length() >= 15
    
    def evaluate_winner(self) -> None:
        if self.bar_cerny_cil_bily.cil_length() >= 15:
            print("vyhral bily")
        else:
            print("vyhral cerny")

    def get_smer(self, hrac) -> int:
        if hrac.barva == "cerny":
            return 1
        else:
            return -1
        
    def clamp(self, value: int, min: int = 0, max: int = 25) -> int:
        if value > max:
            return max
        elif value < min:
            return min
        else:
            return value