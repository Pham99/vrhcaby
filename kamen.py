class Kamen:
    def __init__(self, barva) -> None:
        self.barva = barva

    def get_barva(self):
        return self.barva

    def __str__(self) -> str:
        if self.barva == "cerny":
            return "○"
        else:
            return "●"