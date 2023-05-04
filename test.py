import os
import random
import itertools
from typing import Any

def Dvojkostka():
        kostka1 = random.randint(1,6)
        kostka2 = random.randint(1,6)
        if kostka1 == kostka2:
            return [kostka1]*4
        else:
            return [kostka1, kostka2]
        
def Mozne_kroky(kroky):
    if len(kroky) > 2:
        kroky = list(itertools.accumulate(kroky))
        return kroky
    elif len(kroky) == 2:
        kroky.append(kroky[0] + kroky[1])
    else:
        return kroky
    return kroky

def Tah(self, zacatek, konec, dice):
     krok = konec - zacatek
     if krok in dice:
          self.hracideska[konec].Push(self.hracideska[zacatek].Pop())
          dice.remove(krok)
     else:
        suma_dice = sum(dice)
        while suma_dice - krok != sum(dice):
             temp = dice.pop(krok)
             self.hracideska[temp].Push(self.hracideska[zacatek].Pop())
             zacatek += temp
        return dice

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

class Hrac:

    def __init__(self, colour) -> None:
        self.colour = colour

    def Play(self):
        print("plaaay" + str(self.colour))

class Hrac_CPU(Hrac):

    def __init__(self, colour) -> None:
        super().__init__(colour)
        pass

    def Play(self):
        print("beep boop" + str(self.colour))

def vypocti_mozne_kroky(self, kroky):
    if len(kroky) > 2:
        kroky = list(itertools.accumulate(kroky))
        return kroky
    elif len(kroky) == 2:
        kroky.append(kroky[0] + kroky[1])
    else:
        return kroky
    return kroky

class OObject:
    def __init__(self) -> None:
        pass



# a = Hrac("black")
# b = Hrac_CPU("bruh")
# a.Play()
# b.Play()

# ad = {1: "wow", 2: 1, "fi": [1,2,3,4]}
# b = ad
# print(ad)
# print(ad.keys())
# ad[4] = 50
# print(type(ad["fi"]))
# print(b)

lol = []
print(lol == [])
