class Pretty_dice:
    ceiling = "┌───────┐"
    floor = "└───────┘"
    empty = "│       │"
    center = "│   O   │"
    left = "│ O     │"
    right = "│     O │"
    double = "│ O   O │"
    triple = "│ O O O │"

    @classmethod
    def __get_dice(cls, value):
        match value:
            case 1:
                return cls.empty, cls.center, cls.empty
            case 2:
                return cls.right, cls.empty, cls.left
            case 3:
                return cls.right, cls.center, cls.left
            case 4:
                return cls.double, cls.empty, cls.double
            case 5:
                return cls.double, cls.center, cls.double
            case 6:
                return cls.triple, cls.empty, cls.triple
            case _:
                return "wrong number in list"

    @classmethod    
    def print_dice(cls, seznam):
        if isinstance(seznam, int):
            seznam = [seznam]
        p0, p1, p2, p3, p4 = "","","","",""
        for i in seznam:
            s1, s2, s3 = cls.__get_dice(i)
            p0 += cls.ceiling
            p1 += s1
            p2 += s2
            p3 += s3
            p4 += cls.floor
        print(p0)
        print(p1)
        print(p2)
        print(p3)
        print(p4)

def main():
    Pretty_dice.print_dice([1,2,3,4,5,6])

if __name__ == "__main__":
    main()