import pygame
import os
import random
from Lib.Core.Jugador import Jugador
from Lib.Core.Enemigo import Enemigo
from Lib.Var.Constantes import Constantes

# Inicializar Pygame
pygame.init()

#region Configuración de la pantalla
window = pygame.display.set_mode((Constantes.Ancho, Constantes.Alto))
pygame.display.set_caption("Mega-Runner")
fuente_path = os.path.join("Lib", "Font", "megaman_2.ttf")
Constantes.FONT_LOST = pygame.font.Font(fuente_path, 40)
#endregion

#region Variables globales

enemigos = []
contador_enemigos = 0

#endregion

#region Funciones

def cargar_fondo():
    fondo = pygame.image.load(os.path.join(Constantes.IMAGES_PATH, "fondo.png")).convert_alpha()
    return fondo, fondo.get_rect(), fondo.get_rect(topleft=(fondo.get_rect().width, 0))

def reiniciar_juego():
    global jugador, perdio, contador_enemigos, enemigos
    jugador = Jugador()
    perdio = False
    contador_enemigos = 0
    enemigos.clear()

def mostrar_mensaje_derrota(perdio):
    if perdio:
        texto_perdida = Constantes.FONT_LOST.render("Perdiste.", True, Constantes.RED)
        texto_reintentar = pygame.font.Font(fuente_path, 25).render("Presione R para jugar de nuevo", True, Constantes.RED)
        texto_rect = texto_perdida.get_rect(center=(Constantes.Ancho // 2, Constantes.Alto // 2 - 20))
        texto_reintentar_rect = texto_reintentar.get_rect(center=(Constantes.Ancho // 2, Constantes.Alto // 2 + 20))
        window.blit(texto_perdida, texto_rect)
        window.blit(texto_reintentar, texto_reintentar_rect)

def gestionar_enemigos(contador_enemigos):
    tipo = "rojo" if contador_enemigos % 2 == 0 else "normal"
    nuevo_enemigo = Enemigo(tipo)
    return nuevo_enemigo

def mover_fondo(fondo_rect1, fondo_rect2, fondo_velocidad):
    fondo_rect1.x -= fondo_velocidad
    fondo_rect2.x -= fondo_velocidad
    if fondo_rect1.right <= 0:
        fondo_rect1.x = fondo_rect2.right
    if fondo_rect2.right <= 0:
        fondo_rect2.x = fondo_rect1.right

def gestionar_colisiones():
    global perdio

    for enemigo in enemigos[:]:  
        enemigo.mover()

        if enemigo.rect.right < 0:
            enemigos.remove(enemigo)

        if enemigo.is_active and enemigo.rect.colliderect(jugador.rect):
            if jugador.is_attacking:
                enemigo.perder()
                enemigos.remove(enemigo)
            else:
                enemigo.destruir()
                jugador.perder()
                perdio = True
                break

#endregion

#region  Bucle principal

def bucle_principal():
    global contador_enemigos, perdio, enemigos  # Declarar enemigos como global

    fondo, fondo_rect1, fondo_rect2 = cargar_fondo()
    fondo_velocidad = 2  # Velocidad de desplazamiento del fondo
    reiniciar_juego()

    running = True
    pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(1000, 6000))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jugador.saltar()
                elif event.key == pygame.K_p:
                    jugador.atacar()
                elif event.key == pygame.K_r and perdio:
                    reiniciar_juego()

            elif event.type == pygame.USEREVENT + 1:
                contador_enemigos += 1
                enemigos.append(gestionar_enemigos(contador_enemigos))

                if contador_enemigos % 10 == 0:
                    for enemigo in enemigos:
                        enemigo.velocidad += enemigo.velocidad * 0.05  # Incremento de velocidad

                pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(1000, 6000))

        if not perdio:
            jugador.mover()
            gestionar_colisiones()

            # Mover el fondo
            mover_fondo(fondo_rect1, fondo_rect2, fondo_velocidad)

        # Dibujar fondo y sprites
        window.blit(fondo, fondo_rect1)
        window.blit(fondo, fondo_rect2)
        jugador.dibujar(window)
        for enemigo in enemigos:
            enemigo.dibujar(window)

        mostrar_mensaje_derrota(perdio)
        pygame.display.flip()
        pygame.time.delay(50)

    pygame.quit()

#endregion

# Ejecutar el juego
if __name__ == "__main__":
    bucle_principal()
