# main.py
import pygame
import os
import random
from Lib.Core.Jugador import Jugador
from Lib.Core.Enemigo import Enemigo
from Lib.Core.Trampa import Trampa  
from Lib.Var.Constantes import Constantes
from Lib.Color.Colors import Colors
from Lib.Var.Var import Var  

# Inicializar Pygame
pygame.init()

#region Inicialización

window = pygame.display.set_mode((Constantes.Ancho, Constantes.Alto))
pygame.display.set_caption("Mega-Runner")
fuente_path = os.path.join("Lib", "Font", "megaman_2.ttf")
Constantes.FONT_LOST = pygame.font.Font(fuente_path, 40)
# Instanciar la clase Var
vars = Var()  
vars.cargar_recursos()  

#endregion

#region Funciones

def cargar_fondo():
    fondo = pygame.image.load(os.path.join(Constantes.images_Fondo, "fondo.png")).convert_alpha()
    return fondo, fondo.get_rect(), fondo.get_rect(topleft=(fondo.get_rect().width, 0))

def reiniciar_juego():
    global vars  # Usar la instancia de Var
    vars.jugador = Jugador()
    vars.perdio = False
    vars.contador_enemigos = 0
    vars.contador_trampas = 0
    vars.contador_acciones = 0  
    vars.enemigos.clear()
    vars.trampas.clear()  
    vars.fondo_velocidad = 2  
    vars.nivel_actual = 1  
    vars.mostrar_level_up = False  
    vars.tiempo_level_up = 0  
    vars.vidas = 3

def mostrar_mensajes():
    global vars  # Usar la instancia de Var
    nivel_texto = pygame.font.Font(fuente_path, 15).render(f"Nivel: {vars.nivel_actual}", True, Colors.BLUE)
    window.blit(nivel_texto, (5, 5)) 
    
    velocidad_texto = pygame.font.Font(fuente_path, 10).render(f"Velocidad: {int(vars.fondo_velocidad)}", True, Colors.RED)
    window.blit(velocidad_texto, (600, 5))

    controles_texto = pygame.font.Font(fuente_path, 9).render(f"Controles: 'Espacio' para saltar y 'P' para golpear", True, Colors.BLACK)
    window.blit(controles_texto, (5, 580)) 

    for i in range(vars.vidas):
        window.blit(vars.vida_img, vars.vidas_posiciones[i])

    if vars.mostrar_level_up:
        level_up_texto = Constantes.FONT_LOST.render("Level Up!", True, Colors.BLUE)
        window.blit(level_up_texto, level_up_texto.get_rect(center=(Constantes.Ancho // 2, Constantes.Alto // 2)))
    
    if vars.mostrar_level_up and pygame.time.get_ticks() > vars.tiempo_level_up:
        vars.mostrar_level_up = False  

    if vars.perdio:
        texto_perdida = Constantes.FONT_LOST.render("Perdiste", True, Colors.RED)
        texto_reintentar = pygame.font.Font(fuente_path, 25).render("Presione 'R' para jugar de nuevo", True, Colors.RED)
        window.blit(texto_perdida, texto_perdida.get_rect(center=(Constantes.Ancho // 2, Constantes.Alto // 2 - 20)))
        window.blit(texto_reintentar, texto_reintentar.get_rect(center=(Constantes.Ancho // 2, Constantes.Alto // 2 + 20)))

def gestionar_enemigos():
    global vars  # Usar la instancia de Var
    tipos_enemigos = ["tortuga_verde", "tortuga_roja", "volador"]
    tipo_enemigo = random.choice(tipos_enemigos)
    nuevo_enemigo = Enemigo(tipo_enemigo)
    vars.contador_enemigos += 1
    nuevo_enemigo.velocidad *= (vars.fondo_velocidad * 0.3)
    return nuevo_enemigo

def gestionar_trampas():
    return Trampa()  

def mover_fondo(fondo_rect1, fondo_rect2, velocidad):
    fondo_rect1.x -= velocidad
    fondo_rect2.x -= velocidad
    if fondo_rect1.right <= 0:
        fondo_rect1.x = fondo_rect2.right
    if fondo_rect2.right <= 0:
        fondo_rect2.x = fondo_rect1.right

def gestionar_colisiones():
    global vars  # Usar la instancia de Var

    for enemigo in vars.enemigos[:]:  
        enemigo.mover()
        if enemigo.rect.left < 0:
            vars.contador_acciones += 1  
            vars.enemigos.remove(enemigo) 
        elif enemigo.is_active and enemigo.rect.colliderect(vars.jugador.rect):
            if vars.jugador.is_attacking:
                enemigo.perder()
                vars.enemigos.remove(enemigo)  
                vars.contador_acciones += 1  
            else:
                enemigo.destruir()
                vars.vidas -= 1  
                if vars.vidas <= 0: 
                    vars.jugador.perder()
                    vars.perdio = True
                break 
    for trampa in vars.trampas[:]:  
        trampa.mover(vars.fondo_velocidad)  
        if trampa.rect.right < 0:
            vars.trampas.remove(trampa)  
        if trampa.is_active and trampa.rect.colliderect(vars.jugador.rect):
            vars.vidas -= 1  
            if vars.vidas <= 0:  
                vars.jugador.perder() 
                vars.perdio = True
            break

def aumentar_velocidad():
    global vars  # Usar la instancia de Var
    if vars.contador_acciones >= 5:
        vars.contador_acciones = 0          
        vars.fondo_velocidad *= 1.05   
        vars.nivel_actual += 1
        vars.mostrar_level_up = True
        vars.tiempo_level_up = pygame.time.get_ticks() + 2000  

def manejar_botones(pos):
    global vars  # Usar la instancia de Var
    if vars.boton_play_rect.collidepoint(pos):
        vars.juego_en_pausa = not vars.juego_en_pausa  
    elif vars.boton_hard_rect.collidepoint(pos):       
        vars.fondo_velocidad *= 1.2  

#endregion

#region Bucle principal

def bucle_principal():
    global vars  # Usar la instancia de Var porq saque las vars del main
    fondo, fondo_rect1, fondo_rect2 = cargar_fondo()
    reiniciar_juego()

    running = True
    pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(3000, 7000))  
    pygame.time.set_timer(pygame.USEREVENT + 2, random.randint(5000, 16000))  

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    vars.jugador.saltar()
                elif event.key == pygame.K_p:
                    vars.jugador.atacar()
                elif event.key == pygame.K_r and vars.perdio:
                    reiniciar_juego()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                manejar_botones(event.pos)
            elif event.type == pygame.USEREVENT + 1:
                vars.enemigos.append(gestionar_enemigos())
            elif event.type == pygame.USEREVENT + 2:  
                vars.trampas.append(gestionar_trampas())

        if not vars.perdio and not vars.juego_en_pausa:
            vars.jugador.mover()
            gestionar_colisiones()          
            aumentar_velocidad()
            mover_fondo(fondo_rect1, fondo_rect2, vars.fondo_velocidad)

        window.blit(fondo, fondo_rect1)
        window.blit(fondo, fondo_rect2)
        vars.jugador.dibujar(window)
        for enemigo in vars.enemigos:
            enemigo.dibujar(window)
        for trampa in vars.trampas:  
            trampa.dibujar(window)

        mostrar_mensajes()

        # Dibujar botones
        window.blit(vars.boton_play, vars.boton_play_rect)
        window.blit(vars.boton_hard, vars.boton_hard_rect)
        
        pygame.display.flip()
        pygame.time.delay(50)
    pygame.quit()

#endregion

# Ejecutar el juego
if __name__ == "__main__":
    bucle_principal()
