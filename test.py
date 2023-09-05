
import re

def play(vyber) -> list:
    vyber = vyber.strip().lower()
    vyber = re.sub("( +)", " ", vyber)
    if vyber == "exit" or vyber == "save":
        return vyber
    elif bool(re.fullmatch("[\d]{1,2} [\d]{1,2}", vyber)):
        return vyber
    else:
        return "fail"


results = 0
n = 1
pair = [("4 12", "4 12"),
        ("    12    69    ", "12 69"),
        ("exit", "exit"),
        ("   ExIt   ","exit"),
        ("asdf", "fail"),
        ("   sAVE   ", "save"),
        ("  sav3", "fail")
]

for i in pair:
    vstup = play(i[0])
    print(vstup)
    if vstup == i[1]:
        results += 1
    else:
        print(f"test {n} failed")
    n += 1

print(f"{results}/{len(pair)} passed")

print(bool(re.fullmatch("[\d]{1,2} [\d]{1,2}", "asdf")))

print(list(map(int,"2 3".split(" "))))
print(isinstance([1], list))