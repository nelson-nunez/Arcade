import pygame
import os
from Lib.Core.CharacterInterface import CharacterInterface
from Lib.Var.Constantes import Constantes

class Enemigo(CharacterInterface):
    def __init__(self, tipo="tortuga_verde"):
        self.images = self.cargar_imagenes(Constantes.IMAGES_PATH, tipo)
        # Ajustar la posición vertical dependiendo del tipo de enemigo
        self.rect = self.images["mover"][0].get_rect(topleft=(800, 346 if tipo == "volador" else 396))  # 50px más arriba para voladores
        self.image_index = 0
        self.image = self.images["mover"][self.image_index]
        self.velocidad = 5
        self.is_active = True
        self.is_attacked = False
        self.animacion_terminada = False

    def cargar_imagenes(self, images_path, tipo):
        if tipo == "volador":
            return {
                "mover": [pygame.image.load(os.path.join(images_path, f"b{i}.png")).convert_alpha() for i in range(1, 6)],
                "perder": [pygame.image.load(os.path.join(images_path, f"bd{i}.png")).convert_alpha() for i in range(1, 3)],
                "ganar": [pygame.image.load(os.path.join(images_path, f"k{i}.png")).convert_alpha() for i in range(7, 8)]
            }
        elif tipo == "tortuga_verde":
            return {
                "mover": [pygame.image.load(os.path.join(images_path, f"k{i}.png")).convert_alpha() for i in range(1, 6)],
                "perder": [pygame.image.load(os.path.join(images_path, f"k{i}.png")).convert_alpha() for i in range(9, 11)],
                "ganar": [pygame.image.load(os.path.join(images_path, f"k{i}.png")).convert_alpha() for i in range(7, 8)]
            }
        elif tipo == "tortuga_roja":
            return {
                "mover": [pygame.image.load(os.path.join(images_path, f"k{i}rojo.png")).convert_alpha() for i in range(1, 6)],
                "perder": [pygame.image.load(os.path.join(images_path, f"k{i}.png")).convert_alpha() for i in range(9, 11)],
                "ganar": [pygame.image.load(os.path.join(images_path, f"k{i}.png")).convert_alpha() for i in range(7, 8)]
            }

    def mover(self):
        if self.is_active and not self.is_attacked:
            self.rect.x -= self.velocidad
            self.image_index = (self.image_index + 1) % len(self.images["mover"])
            self.image = self.images["mover"][self.image_index]
            if self.rect.right < 0:
                self.rect.left = 800

    def perder(self):
        if not self.animacion_terminada:
            if self.image_index < len(self.images["perder"]):
                self.image = self.images["perder"][self.image_index]
                self.image_index += 1
            else:
                self.animacion_terminada = True
                self.is_active = False

    def destruir(self):
        self.is_active = False

    def dibujar(self, surface):
        if self.is_active or self.is_attacked:
            surface.blit(self.image, self.rect)
