import pygame
import sys
import random

# Pygame initialisieren
pygame.init()

# Farben definieren
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
GRAU = (128, 128, 128)
ROT = (255, 50, 50)
GRUEN = (50, 255, 50)
BLAU = (50, 50, 255)

# Fenster-Einstellungen
BREITE = 800
HOEHE = 600
BILDSCHIRM = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Zahlenraten")

# Schriften initialisieren
GROSS_SCHRIFT = pygame.font.Font(None, 74)
MITTEL_SCHRIFT = pygame.font.Font(None, 48)
KLEIN_SCHRIFT = pygame.font.Font(None, 36)

class Zahlenraten:
    def __init__(self):
        self.ziel_zahl = random.randint(1, 100)
        self.aktuelle_eingabe = ""
        self.nachricht = "Rate eine Zahl zwischen 1 und 100!"
        self.nachricht_farbe = WEISS
        self.versuche = 0
        self.spiel_vorbei = False
        self.animation_wert = 0
        self.animation_richtung = 1

    def zahl_pruefen(self):
        if not self.aktuelle_eingabe:
            return
        
        self.versuche += 1
        geratene_zahl = int(self.aktuelle_eingabe)
        
        if geratene_zahl == self.ziel_zahl:
            self.nachricht = f"Gewonnen in {self.versuche} Versuchen!"
            self.nachricht_farbe = GRUEN
            self.spiel_vorbei = True
        elif geratene_zahl < self.ziel_zahl:
            self.nachricht = "Höher!"
            self.nachricht_farbe = ROT
        else:
            self.nachricht = "Niedriger!"
            self.nachricht_farbe = BLAU
        
        self.aktuelle_eingabe = ""

    def neues_spiel(self):
        self.__init__()

def hauptprogramm():
    spiel = Zahlenraten()
    clock = pygame.time.Clock()

    while True:
        BILDSCHIRM.fill(SCHWARZ)
        
        # Animation für den Hintergrund
        spiel.animation_wert += 0.02 * spiel.animation_richtung
        if spiel.animation_wert >= 1.0 or spiel.animation_wert <= 0.0:
            spiel.animation_richtung *= -1
        
        # Animierter Hintergrund
        for i in range(10):
            farbe = (int(30 + 20 * spiel.animation_wert), 
                    int(30 + 10 * spiel.animation_wert), 
                    int(50 + 30 * spiel.animation_wert))
            pygame.draw.circle(BILDSCHIRM, farbe, 
                             (BREITE//2, HOEHE//2), 
                             300 - i*30)

        # Titel zeichnen
        titel = GROSS_SCHRIFT.render("Zahlenraten", True, WEISS)
        titel_rect = titel.get_rect(center=(BREITE//2, 80))
        BILDSCHIRM.blit(titel, titel_rect)

        # Nachricht zeichnen
        nachricht = MITTEL_SCHRIFT.render(spiel.nachricht, True, spiel.nachricht_farbe)
        nachricht_rect = nachricht.get_rect(center=(BREITE//2, 180))
        BILDSCHIRM.blit(nachricht, nachricht_rect)

        # Eingabefeld zeichnen
        pygame.draw.rect(BILDSCHIRM, GRAU, (BREITE//2 - 100, 250, 200, 50))
        eingabe = MITTEL_SCHRIFT.render(spiel.aktuelle_eingabe + "▌", True, WEISS)
        eingabe_rect = eingabe.get_rect(center=(BREITE//2, 275))
        BILDSCHIRM.blit(eingabe, eingabe_rect)

        # Versuche anzeigen
        versuche = KLEIN_SCHRIFT.render(f"Versuche: {spiel.versuche}", True, WEISS)
        versuche_rect = versuche.get_rect(center=(BREITE//2, 350))
        BILDSCHIRM.blit(versuche, versuche_rect)

        # Hilfetext
        if not spiel.spiel_vorbei:
            hilfe = KLEIN_SCHRIFT.render("Drücke ENTER zum Raten", True, WEISS)
        else:
            hilfe = KLEIN_SCHRIFT.render("Drücke LEERTASTE für ein neues Spiel", True, WEISS)
        hilfe_rect = hilfe.get_rect(center=(BREITE//2, 500))
        BILDSCHIRM.blit(hilfe, hilfe_rect)

        # Events verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not spiel.spiel_vorbei:
                    if event.key == pygame.K_RETURN and spiel.aktuelle_eingabe:
                        spiel.zahl_pruefen()
                    elif event.key == pygame.K_BACKSPACE:
                        spiel.aktuelle_eingabe = spiel.aktuelle_eingabe[:-1]
                    elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, 
                                     pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, 
                                     pygame.K_8, pygame.K_9] and len(spiel.aktuelle_eingabe) < 3:
                        spiel.aktuelle_eingabe += event.unicode
                elif event.key == pygame.K_SPACE:
                    spiel.neues_spiel()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    hauptprogramm()
