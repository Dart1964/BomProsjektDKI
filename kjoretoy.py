# Remove incorrect inheritance and super() call; define vehicle fields directly
class kjoretoy:
    def __init__(self, registreringsnummer, merke, modell, eier):
        self.registreringsnummer = registreringsnummer
        self.merke = merke
        self.modell = modell
        self.eier = eier

