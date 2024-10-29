import pygame
import os
import random
from Lib.Core.Jugador import Jugador
from Lib.Core.Enemigo import Enemigo
from Lib.Core.Trampa import Trampa  
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
trampas = []  
contador_enemigos = 0
contador_trampas = 0 
contador_acciones = 0 
fondo_velocidad = 2  
nivel_actual = 1 
mostrar_level_up = False  
tiempo_level_up = 0  # Tiempo restante para mostrar el mensaje de Level Up
perdio = False  # Variable para verificar si el jugador ha perdido
jugador = None  # Inicializar jugador

#endregion

#region Funciones

def cargar_fondo():
    fondo = pygame.image.load(os.path.join(Constantes.IMAGES_PATH, "fondo.png")).convert_alpha()
    return fondo, fondo.get_rect(), fondo.get_rect(topleft=(fondo.get_rect().width, 0))

def reiniciar_juego():
    global jugador, perdio, contador_enemigos, enemigos, contador_trampas, trampas, contador_acciones, fondo_velocidad, nivel_actual, mostrar_level_up, tiempo_level_up
    jugador = Jugador()
    perdio = False
    contador_enemigos = 0
    contador_trampas = 0
    contador_acciones = 0  # Reiniciar el contador de acciones
    enemigos.clear()
    trampas.clear()  # Limpiar trampas al reiniciar
    fondo_velocidad = 2  # Reiniciar velocidad del fondo
    nivel_actual = 1  # Reiniciar nivel
    mostrar_level_up = False  # Reiniciar el estado de Level Up
    tiempo_level_up = 0  # Reiniciar el tiempo de Level Up

def mostrar_mensajes():
    global mostrar_level_up, tiempo_level_up  
    # Mostrar el nivel en la parte superior izquierda
    nivel_texto = pygame.font.Font(fuente_path, 15).render(f"Nivel: {nivel_actual}", True, Constantes.BLUE)
    window.blit(nivel_texto, (5, 5)) 
    
    if mostrar_level_up:
        level_up_texto = Constantes.FONT_LOST.render("Level Up!", True, Constantes.BLUE)
        window.blit(level_up_texto, level_up_texto.get_rect(center=(Constantes.Ancho // 2, Constantes.Alto // 2)))
    
    if mostrar_level_up and pygame.time.get_ticks() > tiempo_level_up:
        mostrar_level_up = False  # Ocultar el mensaje después de 3 segundos

    if perdio:
        texto_perdida = Constantes.FONT_LOST.render("Perdiste", True, Constantes.RED)
        texto_reintentar = pygame.font.Font(fuente_path, 25).render("Presione R para jugar de nuevo", True, Constantes.RED)
        window.blit(texto_perdida, texto_perdida.get_rect(center=(Constantes.Ancho // 2, Constantes.Alto // 2 - 20)))
        window.blit(texto_reintentar, texto_reintentar.get_rect(center=(Constantes.Ancho // 2, Constantes.Alto // 2 + 20)))

def gestionar_enemigos():
    global contador_enemigos
    # Definimos una lista de tipos de enemigos
    tipos_enemigos = ["tortuga_verde", "tortuga_roja", "volador"]
    # Elegir un tipo de enemigo aleatorio
    tipo_enemigo = random.choice(tipos_enemigos)
    nuevo_enemigo = Enemigo(tipo_enemigo)
    contador_enemigos += 1
    return nuevo_enemigo

def gestionar_trampas():
    return Trampa()  # Crear una nueva trampa

def mover_fondo(fondo_rect1, fondo_rect2, velocidad):
    fondo_rect1.x -= velocidad
    fondo_rect2.x -= velocidad
    if fondo_rect1.right <= 0:
        fondo_rect1.x = fondo_rect2.right
    if fondo_rect2.right <= 0:
        fondo_rect2.x = fondo_rect1.right

def gestionar_colisiones():
    global perdio, contador_acciones

    for enemigo in enemigos[:]:  
        enemigo.mover()
        # Verificar si el enemigo ha salido de la pantalla por la izquierda
        if enemigo.rect.left < 0:
            contador_acciones += 1  # Incrementar el contador de acciones
            enemigos.remove(enemigo) 
        # Verificar colisiones con el jugador
        elif enemigo.is_active and enemigo.rect.colliderect(jugador.rect):
            if jugador.is_attacking:
                enemigo.perder()
                enemigos.remove(enemigo)  
                contador_acciones += 1  
            else:
                enemigo.destruir()
                jugador.perder()
                perdio = True
                break 
    for trampa in trampas[:]:  
        trampa.mover(fondo_velocidad) 
        if trampa.rect.right < 0:
            trampas.remove(trampa)  
        if trampa.is_active and trampa.rect.colliderect(jugador.rect):
            jugador.perder() 
            perdio = True
            break


def aumentar_velocidad():
    global fondo_velocidad, contador_acciones, nivel_actual, mostrar_level_up, tiempo_level_up
    if contador_acciones >= 5:
        contador_acciones = 0  
        fondo_velocidad *= 1.05
        nivel_actual += 1
        mostrar_level_up = True
        tiempo_level_up = pygame.time.get_ticks() + 3000 

#endregion

#region  Bucle principal

def bucle_principal():
    global contador_enemigos, contador_trampas, perdio, enemigos, trampas, contador_acciones, fondo_velocidad, nivel_actual, mostrar_level_up, tiempo_level_up  
    fondo, fondo_rect1, fondo_rect2 = cargar_fondo()
    reiniciar_juego()

    running = True
    pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(3000, 7000))  # Temporizador para enemigos
    pygame.time.set_timer(pygame.USEREVENT + 2, random.randint(5000, 16000))  # Temporizador para trampas

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
                enemigos.append(gestionar_enemigos())
            elif event.type == pygame.USEREVENT + 2:  
                trampas.append(gestionar_trampas())

        if not perdio:
            jugador.mover()
            gestionar_colisiones()          
            aumentar_velocidad()
            mover_fondo(fondo_rect1, fondo_rect2, fondo_velocidad)

        # Dibujar fondo y sprites
        window.blit(fondo, fondo_rect1)
        window.blit(fondo, fondo_rect2)
        jugador.dibujar(window)
        for enemigo in enemigos:
            enemigo.dibujar(window)
        for trampa in trampas:  
            trampa.dibujar(window)

        # Mostrar nivel actual aca porq dsps se resetea
        mostrar_mensajes()
        pygame.display.flip()
        pygame.time.delay(50)
    pygame.quit()

#endregion

# Ejecutar el juego
if __name__ == "__main__":
    bucle_principal()
