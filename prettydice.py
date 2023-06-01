class Pretty_dice:
    __ceiling = "┌───────┐"
    __floor = "└───────┘"
    __empty = "│       │"
    __center = "│   ○   │"
    __left = "│ ○     │"
    __right = "│     ○ │"
    __double = "│ ○   ○ │"
    __triple = "│ ○ ○ ○ │"

    @classmethod
    def __get_dice(cls, value: int) -> tuple:
        match value:
            case 1:
                return cls.__empty, cls.__center, cls.__empty
            case 2:
                return cls.__right, cls.__empty, cls.__left
            case 3:
                return cls.__right, cls.__center, cls.__left
            case 4:
                return cls.__double, cls.__empty, cls.__double
            case 5:
                return cls.__double, cls.__center, cls.__double
            case 6:
                return cls.__triple, cls.__empty, cls.__triple
            case _:
                return "wrong number in list"

    @classmethod    
    def print_dice(cls, seznam: list) -> None:
        if isinstance(seznam, int):
            seznam = [seznam]
        p0, p1, p2, p3, p4 = "","","","",""
        for i in seznam:
            s1, s2, s3 = cls.__get_dice(i)
            p0 += cls.__ceiling
            p1 += s1
            p2 += s2
            p3 += s3
            p4 += cls.__floor
        print(p0)
        print(p1)
        print(p2)
        print(p3)
        print(p4)

def main():
    Pretty_dice.__ceiling = "lol"
    print(Pretty_dice.__ceiling)
    Pretty_dice.print_dice([1,2,3,4,5,6])

if __name__ == "__main__":
    main()