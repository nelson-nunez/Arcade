import pygame
import os
from Lib.Var.Constantes import Constantes 
from Lib.Core.CharacterInterface import CharacterInterface

class Jugador(CharacterInterface):
    def __init__(self):
        # Carga de imágenes
        self.images = {
            "quieto": pygame.image.load(os.path.join(Constantes.images_Jugador, "1.png")).convert_alpha(),
            "mover": [pygame.image.load(os.path.join(Constantes.images_Jugador, f"{i}.png")).convert_alpha() for i in range(2, 5)],
            "saltar": [pygame.image.load(os.path.join(Constantes.images_Jugador, f"{i}.png")).convert_alpha() for i in range(5, 8)],
            "atacar": [pygame.image.load(os.path.join(Constantes.images_Jugador, f"{i}.png")).convert_alpha() for i in [8, 9, 10, 11, 12, 11, 10, 9, 8]],
            "perder": [pygame.image.load(os.path.join(Constantes.images_Jugador, f"d{i}.png")).convert_alpha() for i in range(1, 3)]
        }
        
        # Configuración inicial
        self.rect = self.images["quieto"].get_rect(topleft=(100, 400))
        self.image = self.images["quieto"]
        self.image_index = 0
        self.is_jumping = False
        self.can_double_jump = False  # Nueva variable para controlar el doble salto
        self.jump_speed = 15
        self.double_jump_speed = 10  # Velocidad del segundo salto
        self.gravity = 1
        self.jump_offset = 0
        self.is_attacking = False  
        self.animacion_terminada = False       
        self.is_active = True

    def dibujar(self, surface):
        surface.blit(self.image, self.rect)

    def mover(self):
        if not self.is_jumping and not self.is_attacking:
            self.image_index = (self.image_index + 1) % len(self.images["mover"])
            self.image = self.images["mover"][self.image_index]

        if self.is_jumping:
            self.rect.y += self.jump_offset
            self.jump_offset += self.gravity
            
            if self.image_index < len(self.images["saltar"]):
                self.image = self.images["saltar"][self.image_index]
                self.image_index += 1
            
            # Detectar el suelo para reiniciar el salto
            if self.rect.y >= 400:  
                self.rect.y = 400
                self.is_jumping = False
                self.can_double_jump = False  # Reiniciar el estado de salto doble
                self.image_index = 0

        if self.is_attacking:
            if self.image_index < len(self.images["atacar"]):
                self.image = self.images["atacar"][self.image_index]
                self.image_index += 1
            else:
                self.is_attacking = False
                self.image_index = 0

    def ganar(self):
        # Continua porque nose que iba a poner acá
        pass

    def perder(self):
        if self.image_index < len(self.images["perder"]):
            self.image = self.images["perder"][self.image_index]
            self.image_index += 1
        else:
            self.animacion_terminada = True
            self.is_active = False

    def destruir(self):
        self.is_active = False

    def saltar(self):
        if not self.is_jumping:
            # Primer salto
            self.is_jumping = True
            self.jump_offset = -self.jump_speed
            self.image_index = 0
            self.can_double_jump = True  # Habilitar salto doble
        elif self.can_double_jump:
            # Segundo salto
            self.jump_offset = -self.double_jump_speed * 1.5  # Aumentar la altura del salto
            self.can_double_jump = False  # Deshabilitar salto doble después de usarlo
            self.image_index = 0

    def atacar(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.image_index = 0 
