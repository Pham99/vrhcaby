class HraciPole:
    def __init__(self) -> None:
        self.__seznam = list()

    def push(self, value):
        self.__seznam.append(value)

    def pop(self):
        if len(self.__seznam) == 0:
            print("i cannot")
        else:
            return self.__seznam.pop()
        
    def peek(self):
        if len(self.__seznam) > 0:
            return self.__seznam[-1].get_barva()
        else:
            return "neutral"
        
    def length(self):
        return len(self.__seznam)
        
    def __str__(self) -> str:
        if self.peek() == "cerny":
            symbol = "o"
        else:
            symbol = "●"
        return symbol * self.length()
        #return str(list(map(str,self.__seznam))).replace("cerny", "o").replace("bily", "●")

class Bar(HraciPole):
    def __init__(self, barva) -> None:
        super().__init__()
        self.__cil = list()
        self.barva = barva

    def push(self, value):
        if value.get_barva() == self.barva:
            self.__seznam.append(value)
        else:
            self.__cil.append(value)

    