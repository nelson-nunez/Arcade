import pygame
import os
from Lib.Core.CharacterInterface import CharacterInterface
from Lib.Var.Constantes import Constantes

class Trampa:
    def __init__(self):
        self.image = pygame.image.load(os.path.join(Constantes.images_Trampa, "trampa.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(800, 400)) 
        self.is_active = True

    def mover(self, velocidad_fondo):
        if self.is_active:
            self.rect.x -= velocidad_fondo  
            # Mover a la velocidad del fondo

    def dibujar(self, surface):
        if self.is_active:
            surface.blit(self.image, self.rect)

    def destruir(self):
        self.is_active = False

    def perder(self):
        # Continua nomas
        pass
