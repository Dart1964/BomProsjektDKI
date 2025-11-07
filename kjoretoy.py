class kjoretoy(kjoretoypassering):
    def __init__(self, registreringsnummer, merke, modell, eier):
        super().__init__(self, registreringsnummer)
        self.merke = merke
        self.modell = modell
        self.eier = eier
