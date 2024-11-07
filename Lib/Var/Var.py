# Lib/Var/Var.py
import pygame
import os
from Lib.Var.Constantes import Constantes

class Var:
    def __init__(self):
        self.enemigos = []
        self.trampas = []
        self.contador_enemigos = 0
        self.contador_trampas = 0
        self.contador_acciones = 0
        self.fondo_velocidad = 2
        self.nivel_actual = 1
        self.mostrar_level_up = False
        self.tiempo_level_up = 0
        self.perdio = False
        self.jugador = None
        self.juego_en_pausa = False
        
        # Inicialización de las vidas
        self.vidas = 3  # Tres vidas iniciales
        self.vida_img = None  # Inicializaremos más tarde
        self.vidas_posiciones = [(5 + i * 35, 30) for i in range(self.vidas)]
        
        # Cargar imágenes de los botones
        self.boton_play = None  # Inicializaremos más tarde
        self.boton_hard = None  # Inicializaremos más tarde
        self.boton_play_rect = None  # Inicializaremos más tarde
        self.boton_hard_rect = None  # Inicializaremos más tarde

    def cargar_recursos(self):
        # Cargar imágenes y otros recursos aquí
        self.vida_img = pygame.image.load(os.path.join(Constantes.images_Iconos, "vida.png")).convert_alpha()
        self.boton_play = pygame.image.load(os.path.join(Constantes.images_Iconos, "play.png")).convert_alpha()
        self.boton_hard = pygame.image.load(os.path.join(Constantes.images_Iconos, "hard.png")).convert_alpha()
        
        # Posiciones de los botones
        boton_y = Constantes.Alto - 10 - self.boton_play.get_height()
        self.boton_play_rect = self.boton_play.get_rect(center=(Constantes.Ancho // 2 - self.boton_play.get_width() - 15, boton_y))
        self.boton_hard_rect = self.boton_hard.get_rect(center=(Constantes.Ancho // 2 + self.boton_hard.get_width() + 15, boton_y))
