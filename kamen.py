class Kamen:
    def __init__(self, barva: str, historie_pozic: list, kill_count: int=0) -> None:
        self.barva = barva
        self.historie_pozic = historie_pozic
        self.kill_count = kill_count

    def get_barva(self):
        return self.barva
    
    def add_position(self, position):
        self.historie_pozic.append(position)

    def add_kill(self):
        self.kill_count += 1

    def __str__(self) -> str:
        if self.barva == "cerny":
            return "○"
        else:
            return "●"