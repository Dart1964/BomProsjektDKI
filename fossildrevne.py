"""Adapter-modul for fossildrevne kjøretøy som arver fra kjoretoy.

Obs: denne filen forutsetter at `kjoretoy.py` eksporterer en (lavere-/samme-)navngitt klasse.
"""
from kjoretoy import kjoretoy
class fossildrevne(kjoretoy):
    """Superklasse for fossildrevne kjøretøy.

    Gir felles initialisering for merke, modell, eier og registreringsnummer.
    """
    def __init__(self, registreringsnummer, merke, modell, eier):
        """Initialiserer et fossildrevet kjøretøy.

        Parametre:
        - registreringsnummer (str): kjøretøyets registreringsnummer
        - merke (str): bilmerke
        - modell (str): modellnavn
        - eier (str): eierens navn
        """
        # explicit call (also correct)
        kjoretoy.__init__(self, registreringsnummer, merke, modell, eier)