class HraciPole:
    def __init__(self) -> None:
        self._seznam = list()

    def push(self, object):
        self._seznam.append(object)

    def pop(self):
        if len(self._seznam) == 0:
            print("i cannot")
        else:
            return self._seznam.pop()
        
    def peek(self):
        if len(self._seznam) > 0:
            return self._seznam[-1].get_barva()
        else:
            return "neutral"
        
    def get_kamen(self):
        return self._seznam[-1]
        
    def length(self):
        return len(self._seznam)
        
    def __str__(self) -> str:
        return str(self._seznam[-1])

    def print_pole(self):
        if self.peek() == "cerny":
            symbol = "o"
        else:
            symbol = "●"
        return symbol * self.length()
    
    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= len(self._seznam) - 1:
            x = self._seznam[self.n]
            self.n += 1
            return x
        else:
            raise StopIteration
    
class Bar(HraciPole):
    def __init__(self, barva) -> None:
        super().__init__()
        self.__cil = list()
        self.barva = barva

    def push(self, object):
        if object.get_barva() == self.barva:
            self._seznam.append(object)
        else:
            self.__cil.append(object)
    
    def print_cil(self):
        if self.barva == "cerny":
            symbol = "●"
        else:
            symbol = "o"
        return symbol * self.cil_length()
    
    def cil_length(self):
        return len(self.__cil)
    
    def print_pole(self):
        return super().print_pole()
    
    def __str__(self) -> str:
        return str(len(self.__cil))
    
    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= len(self._seznam) - 1:
            x = self._seznam[self.n]
            self.n += 1
            return x
        else:
            raise StopIteration

def main():
    pass

if __name__ == "__main":
    main()