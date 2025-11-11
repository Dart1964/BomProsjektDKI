"""Eksempelskript som viser hvordan registrere kjøretøy og passeringer.

Oppretter et register, legger til noen kjøretøy og simulerer passeringer i Trafikksystemet.
Skriver ut dato/time med flest passeringer og kjøretøyet med flest passeringer.
"""

from kjoretoy import Diesel, Fossildrevne, Bensin95, Elektriske
from funksjon import KjoretoyPassering, Trafikksystem, Kjoretoyregister
from datetime import date

# --- Eksempel på bruk ---
if __name__ == "__main__":
    register = Kjoretoyregister()

    bil1 = Diesel("Volkswagen", "Golf", "Ola Nordmann", "AB12345")
    bil2 = Bensin95("Toyota", "Corolla", "Kari Olsen", "CD67890")
    bil3 = Elektriske("Tesla", "Model 3", "Per Hansen", "EF11111")

    for bil in [bil1, bil2, bil3]:
        register.legg_til(bil)

    system = Trafikksystem(register)

    system.legg_til_passering(KjoretoyPassering(date(2025, 11, 10), 8, "AB12345"))
    system.legg_til_passering(KjoretoyPassering(date(2025, 11, 10), 9, "AB12345"))
    system.legg_til_passering(KjoretoyPassering(date(2025, 11, 10), 8, "CD67890"))
    system.legg_til_passering(KjoretoyPassering(date(2025, 11, 11), 9, "EF11111"))
    system.legg_til_passering(KjoretoyPassering(date(2025, 11, 11), 9, "AB12345"))
    system.legg_til_passering(KjoretoyPassering(date(2025, 11, 11), 9, "AB12345"))

    dato, time = system.flest_passeringer_dato_og_time()
    if dato:
        print(f"Flest passeringer på dato {dato.strftime('%d.%m.%Y')}, time {time}:00–{time+1}:00.")
    kjoretoy, antall = system.flest_passeringer_kjoretoy()
    if kjoretoy:
        print(f"Kjøretøyet med flest passeringer: {kjoretoy} ({antall} ganger).")