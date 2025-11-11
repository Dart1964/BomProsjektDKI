from kjoretoy import kjoretoy
class fossildrevne(kjoretoy):
    def __init__(self, registreringsnummer, merke, modell, eier):
        # explicit call (also correct)
        kjoretoy.__init__(self, registreringsnummer, merke, modell, eier)