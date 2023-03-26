import random
import itertools

def Dvojkostka():
        kostka1 = random.randint(1,6)
        kostka2 = random.randint(1,6)
        if kostka1 == kostka2:
            return [kostka1]*4
        else:
            return [kostka1, kostka2]
        
def Mozne_kroky(self, kroky):
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