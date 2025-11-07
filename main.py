import time

class kjoretoypassering:
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


def flest_passeringer_dato():
    pass  

def flest_passeringer_time():
    pass
        
def flest_passeringer_kjoretoy():
    pass
    
