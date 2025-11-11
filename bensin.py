"""Modul for bensindrevne kjøretøy."""
from fossildrevne import fossildrevne
class bensin(fossildrevne):
    """Klasse som representerer en bensindrevet bil (arver fra fossildrevne)."""
    def __init__(self, registreringsnummer, merke, modell, eier):
        """Initialiserer en bensinbil.

        Parametre:
        - registreringsnummer (str)
        - merke (str)
        - modell (str)
        - eier (str)
        """
        super().__init__(registreringsnummer, merke, modell, eier)