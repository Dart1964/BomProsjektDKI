"""Definerer dataklasser for kjøretøy.

Inneholder:
- Kjoretoy: basisreprensentasjon av et kjøretøy.
- Fossildrevne: mellomklasse for fossildrevne kjøretøy.
- Diesel, Bensin95: konkrete fossildrevne typer.
- Elektriske: konkret klasse for elektriske kjøretøy.
"""

class Kjoretoy:
    """
    Representerer et kjøretøy.
    Attributter:
        merke (str): Bilmerke.
        modell (str): Modellnavn.
        eier (str): Eierens navn.
        registreringsnummer (str): Unik identifikator.
    """
    def __init__(self, merke, modell, eier, registreringsnummer):
        self.merke = merke
        self.modell = modell
        self.eier = eier
        self.registreringsnummer = registreringsnummer

    def __str__(self):
        return f"{self.merke} {self.modell} ({self.registreringsnummer})"


class Fossildrevne(Kjoretoy):
    """Superklasse for bensin- og dieseldrevne biler."""
    def __init__(self, merke, modell, eier, registreringsnummer, drivstoff):
        super().__init__(merke, modell, eier, registreringsnummer)
        self.drivstoff = drivstoff

    def __str__(self):
        return f"{super().__str__()} - Fossildrevet ({self.drivstoff})"


class Diesel(Fossildrevne):
    """Dieseldrevet bil."""
    def __init__(self, merke, modell, eier, registreringsnummer):
        super().__init__(merke, modell, eier, registreringsnummer, "Diesel")


class Bensin95(Fossildrevne):
    """Bensindrevet bil (blyfri 95)."""
    def __init__(self, merke, modell, eier, registreringsnummer):
        super().__init__(merke, modell, eier, registreringsnummer, "Bensin 95")


class Elektriske(Kjoretoy):
    """Elektrisk bil."""
    def __init__(self, merke, modell, eier, registreringsnummer):
        super().__init__(merke, modell, eier, registreringsnummer)

    def __str__(self):
        return f"{super().__str__()} - Elektrisk"