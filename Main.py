import pygame
import random
from Lib.Core.Jugador import Jugador 
from Lib.Core.Enemigo import Enemigo
from Lib.Var.Constantes import Constantes  # Asegúrate de importar las constantes

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
window = pygame.display.set_mode((Constantes.Ancho, Constantes.Alto))
pygame.display.set_caption("Juego: Jugador vs enemigo")

# Asignar la fuente a la constante de Vars
Constantes.FONT_LOST = pygame.font.SysFont(None, 100)

# Instancias de los personajes
jugador = Jugador()
enemigo = Enemigo()
perdio = False
perdio_anim_index = 0

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.saltar()
            elif event.key == pygame.K_p:
                jugador.activar_poder()
        elif event.type == pygame.USEREVENT + 1:
            if enemigo.animacion_terminada:
                enemigo = Enemigo()  # Crea un nuevo enemigo

    # Lógica del juego
    if not perdio:
        enemigo.mover()
        jugador.actualizar_posicion()

    # Verificar colisión
    if enemigo.is_active and enemigo.rect.colliderect(jugador.rect):
        if jugador.is_powering:
            enemigo.derrota()
        else:
            enemigo.destruir()
            jugador.derrota()
            perdio = True

    # Dibuja en la ventana
    window.fill(Constantes.WHITE)  # Usa el color blanco de las constantes
    jugador.dibujar(window)
    enemigo.dibujar(window)
    
    # Muestra animación de derrota
    if perdio:
        texto_perdida = Constantes.FONT_LOST.render("Perdiste. Intentar de nuevo?", True, Constantes.RED) 
        texto_rect = texto_perdida.get_rect(center=(Constantes.Ancho // 2, Constantes.Alto // 2))
        window.blit(texto_perdida, texto_rect)

    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
