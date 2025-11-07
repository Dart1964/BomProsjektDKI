import os
import time;
    def __init__(self, dato, time, registreringsnummer):
        self.dato = dato
        self.time = time
        self.registreringsnummer = registreringsnummer
        

class kjoretoy(kjoretoypassering):
    def __init__(self, registreringsnummer, merke, modell, eier):
        super().__init__(self, registreringsnummer)
        self.merke = merke
        self.modell = modell
        self.eier = eier


class fossildrevne(kjoretoy):
    def __init__(self, registreringsnummer, merke, modell, eier):
        super().__init__(self, registreringsnummer, merke, modell, eier)

class elektriske(kjoretoy):
    def __init__(self, registreringsnummer, merke, modell, eier):
        super().__init__(self, registreringsnummer, merke, modell, eier)

class bensin(fossildrevne):
    def __init__(self, registreringsnummer, merke, modell, eier):
        super().__init__(self, registreringsnummer, merke, modell, eier)

class diesel(fossildrevne):
    def __init__(self, registreringsnummer, merke, modell, eier):
        super().__init__(self, registreringsnummer, merke, modell, eier)

eksempel_passeringer = [
    kjoretoypassering(1761955200, 8,  "AB12345"),  # 2025-11-01 08:00
    kjoretoypassering(1761955200, 12, "CD98765"),  # 2025-11-01 12:00
    kjoretoypassering(1762041600, 7,  "EF45678"),  # 2025-11-02 07:00
    kjoretoypassering(1762041600, 18, "GH23456"),  # 2025-11-02 18:00
    kjoretoypassering(1762128000, 9,  "IJ34567"),  # 2025-11-03 09:00
    kjoretoypassering(1762128000, 21, "KL76543"),  # 2025-11-03 21:00
    kjoretoypassering(1762214400, 13, "MN11223"),  # 2025-11-04 13:00
    kjoretoypassering(1762214400, 16, "OP33445"),  # 2025-11-04 16:00
    kjoretoypassering(1762300800, 6,  "QR55667"),  # 2025-11-05 06:00
    kjoretoypassering(1762300800, 14, "ST77889"),  # 2025-11-05 14:00
]

diesel_kjoretoy = [
    diesel("AB12345", "Volvo", "V70", "Ola Nordmann"),
    diesel("GH23456", "Ford", "Focus", "Kari Nordmann"),
    diesel("MN11223", "VW", "Passat", "Per Hansen"),
]

bensin_kjoretoy = [
    bensin("CD98765", "Toyota", "Corolla", "Anne Olsen"),
    bensin("EF45678", "Honda", "Civic", "Lars Johansen"),
    bensin("OP33445", "Mazda", "3", "Ida Berg"),
]

elektriske_kjoretoy = [
    elektriske("IJ34567", "Tesla", "Model 3", "Jon Berg"),
    elektriske("KL76543", "Nissan", "Leaf", "Eva Hansen"),
    elektriske("QR55667", "VW", "ID.4", "Mats Larsen"),
    elektriske("ST77889", "Hyundai", "Kona Electric", "Siri Dahl"),
]


def flest_passeringer_dato():
    pass  

def flest_passeringer_time():
    pass
        
def flest_passeringer_kjoretoy():
    for k in eksempel_passeringer:
        k.dato