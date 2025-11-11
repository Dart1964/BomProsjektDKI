from collections import defaultdict, Counter

class Kjoretoyregister:
    """
    Register over alle kjøretøy.
    """
    def __init__(self):
        self.register = {}

    def legg_til(self, kjoretoy):
        """Legg til et kjøretøy i registeret."""
        self.register[kjoretoy.registreringsnummer] = kjoretoy

    def finn(self, registreringsnummer):
        """Finn kjøretøy basert på registreringsnummer."""
        return self.register.get(registreringsnummer)


class KjoretoyPassering:
    """
    Representerer én registrert passering.
    Attributter:
        dato (int): Dato i f.eks. format 20251111.
        time (int): Timeintervall (f.eks. 8 for 08–09).
        registreringsnummer (str): Kjøretøyets registreringsnummer.
    """
    def __init__(self, dato, time, registreringsnummer):
        self.dato = dato
        self.time = time
        self.registreringsnummer = registreringsnummer


class Trafikksystem:
    """
    Hovedklasse som kobler passeringer med kjøretøyregisteret.
    Beregner:
      - Datoen med flest passeringer og timen med flest den dagen.
      - Kjøretøyet med flest passeringer.
    """
    def __init__(self, register):
        self.register = register
        self.passeringer = []

    def legg_til_passering(self, passering):
        self.passeringer.append(passering)

    def flest_passeringer_dato_og_time(self):
        """Returnerer datoen med flest passeringer og timen med flest passeringer den dagen."""
        if not self.passeringer:
            return None, None

        datoer = Counter(p.dato for p in self.passeringer)
        mest_dato = datoer.most_common(1)[0][0]

        timer = Counter(p.time for p in self.passeringer if p.dato == mest_dato)
        mest_time = timer.most_common(1)[0][0]
        return mest_dato, mest_time

    def flest_passeringer_kjoretoy(self):
        """Returnerer kjøretøyet med flest passeringer og type."""
        if not self.passeringer:
            return None

        counts = Counter(p.registreringsnummer for p in self.passeringer)
        mest_nr, antall = counts.most_common(1)[0]
        kjoretoy = self.register.finn(mest_nr)
        return kjoretoy, antall