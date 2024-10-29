import pygame
import os
from Lib.Core.CharacterInterface import CharacterInterface
from Lib.Var.Constantes import Constantes  # Asegúrate de importar las constantes

class Enemigo(CharacterInterface):
    def __init__(self):
        # Carga las imágenes al inicializar el enemigo
        images_path = os.path.join(Constantes.IMAGES_PATH)  # Usa la ruta de imágenes de las constantes
        self.images = self.cargar_imagenes(images_path)
        self.rect = self.images["move"][0].get_rect(topleft=(700, 300))  # Ajusta la posición inicial
        self.image_index = 0
        self.image = self.images["move"][self.image_index]
        self.velocidad = 5
        self.is_active = True
        self.is_attacked = False
        self.animacion_terminada = False

    def cargar_imagenes(self, images_path):
        # Carga las imágenes del enemigo
        return {
            "move": [pygame.image.load(os.path.join(images_path, f"k{i}.png")).convert_alpha() for i in range(1, 6)],
            "attacked": [pygame.image.load(os.path.join(images_path, f"k{i}.png")).convert_alpha() for i in range(6, 11)]
        }

    def mover(self):
        if self.is_active and not self.is_attacked:
            self.rect.x -= self.velocidad
            self.image_index = (self.image_index + 1) % len(self.images["move"])
            self.image = self.images["move"][self.image_index]
            if self.rect.right < 0:
                self.rect.left = 800  # Reinicia la posición si sale de la pantalla

    def derrota(self):
        if not self.animacion_terminada:
            if self.image_index < len(self.images["attacked"]):
                self.image = self.images["attacked"][self.image_index]
                self.image_index += 1
            else:
                self.animacion_terminada = True
                self.is_active = False

    def destruir(self):
        self.is_active = False  # Cambia el estado a no activo

    def dibujar(self, surface):
        if self.is_active or self.is_attacked:
            surface.blit(self.image, self.rect)
