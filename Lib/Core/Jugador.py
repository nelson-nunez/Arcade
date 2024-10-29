import pygame
import os
from Lib.Core.CharacterInterface import CharacterInterface
from Lib.Var.Constantes import Constantes  # Asegúrate de importar las constantes

class Jugador(CharacterInterface):
    def __init__(self):
        # Carga de imágenes
        images_path = os.path.join(Constantes.IMAGES_PATH)  # Usa la ruta de imágenes de las constantes
        self.images = {
            "stand": pygame.image.load(os.path.join(images_path, "1.png")).convert_alpha(),
            "move": [pygame.image.load(os.path.join(images_path, f"{i}.png")).convert_alpha() for i in range(2, 5)],
            "jump": [pygame.image.load(os.path.join(images_path, f"{i}.png")).convert_alpha() for i in range(5, 8)],
            "power": [pygame.image.load(os.path.join(images_path, f"{i}.png")).convert_alpha() for i in [8, 9, 10, 9]],
            "attacked": [pygame.image.load(os.path.join(images_path, f"d{i}.png")).convert_alpha() for i in range(1, 3)]
        }

        # Configuración inicial
        self.rect = self.images["stand"].get_rect(topleft=(100, 300))
        self.image_index = 0
        self.image = self.images["stand"]
        self.estado = 1
        self.is_jumping = False
        self.is_powering = False
        self.jump_speed = 15
        self.gravity = 1
        self.jump_offset = 0
        self.animacion_terminada = False

    def mover(self):
        self.image_index = (self.image_index + 1) % len(self.images["move"])
        self.image = self.images["move"][self.image_index]

    def saltar(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_offset = -self.jump_speed
            self.image_index = 0

    def activar_poder(self):
        if not self.is_powering:
            self.is_powering = True
            self.image_index = 0

    def actualizar_posicion(self):
        if self.is_jumping:
            self.rect.y += self.jump_offset
            self.jump_offset += self.gravity
            if self.image_index < len(self.images["jump"]):
                self.image = self.images["jump"][self.image_index]
                self.image_index += 1
            if self.rect.y >= 300:
                self.rect.y = 300
                self.is_jumping = False
        elif self.is_powering:
            if self.image_index < len(self.images["power"]):
                self.image = self.images["power"][self.image_index]
                self.image_index += 1
            else:
                self.image_index = 0
                self.is_powering = False
        else:
            self.mover()

    def derrota(self):
        if not self.animacion_terminada:
            if self.image_index < len(self.images["attacked"]):
                self.image = self.images["attacked"][self.image_index]
                self.image_index += 1
            else:
                self.animacion_terminada = True

    def destruir(self):
        self.is_active = False  # Cambia el estado a no activo
        
    def dibujar(self, surface):
        surface.blit(self.image, self.rect)
