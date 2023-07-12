import pygame
import sys
import random
import speech_recognition as sr

FONDO = 'fondo.jpeg'
PATO = 'pato.png'
MUSICA = 'Shinrin-Yoku.ogg'

pygame.init()

#Configuración:
fondo_original = pygame.image.load(FONDO)
fondo = pygame.transform.scale(fondo_original,(800,600))
personaje_original = pygame.image.load(PATO)
personaje = pygame.transform.scale(personaje_original,(80,80))
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Altas mueve al pato!')
pygame.display.set_icon(personaje)
musica = pygame.mixer.music.load(MUSICA)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

ultimo_flip = 'izq'
pos_x = 100
pos_y = 500
idle = False
ultimo_tiempo = 0

#Invertir imagen:
def image_flip(personaje):
    return pygame.transform.flip(personaje, True, False)


#Movimiento del personaje:
def move_up(pos_y):
    if pos_y > 0:
        pos_y -= 10
    return pos_y


def move_down(pos_y):
    if pos_y < 520:
        pos_y += 10
    return pos_y


def move_right(pos_x, ultimo_flip, personaje):
    if pos_x < 720:
        if ultimo_flip == 'izq':
            ultimo_flip = 'der'
            personaje = image_flip(personaje)
            pos_x += 10
        else:
            pos_x += 10
    return [pos_x, ultimo_flip, personaje]


def move_left(pos_x, ultimo_flip, personaje):
    if pos_x > 0:
        if ultimo_flip == 'der':
            ultimo_flip = 'izq'
            personaje = image_flip(personaje)
            pos_x -= 10
        else:
            pos_x -= 10
    return [pos_x, ultimo_flip, personaje]


#Movimiento automático:
def move_idle(pos_x, pos_y, ultimo_flip, personaje):
    direcciones = ['arriba','abajo','derecha','izquierda']
    eleccion = random.choice(direcciones)
    match eleccion:
        case 'arriba':
            pos_y = move_up(pos_y)
        case 'abajo':
            pos_y = move_down(pos_y)
        case 'derecha':
            valores = move_right(pos_x, ultimo_flip, personaje)
            pos_x = valores[0]
            ultimo_flip = valores[1]
            personaje = valores[2]
        case 'izquierda':
            valores = move_left(pos_x, ultimo_flip, personaje)
            pos_x = valores[0]
            ultimo_flip = valores[1]
            personaje = valores[2]
    return [pos_x, pos_y, ultimo_flip, personaje]


#Movimiento por voz:
def move_voice(pos_x, pos_y, ultimo_flip, personaje):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        texto = r.recognize_google(audio, language="es-ES")
        match texto:
            case 'arriba':
                pos_y = move_up(pos_y)
            case 'abajo':
                pos_y = move_down(pos_y)
            case 'derecha':
                valores = move_right(pos_x, ultimo_flip, personaje)
                pos_x = valores[0]
                ultimo_flip = valores[1]
                personaje = valores[2]
            case 'izquierda':
                valores = move_left(pos_x, ultimo_flip, personaje)
                pos_x = valores[0]
                ultimo_flip = valores[1]
                personaje = valores[2]
        return [pos_x, pos_y, ultimo_flip, personaje]


#Bucle del juego:
while True:
    voice = False
    #Eventos:
    events = pygame.event.get()
    for event in events:
        #Cerrar el juego:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Teclas presionadas:
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pos_y = move_up(pos_y)
            elif event.key == pygame.K_DOWN:
                pos_y = move_down(pos_y)
            elif event.key == pygame.K_RIGHT:
                valores = move_right(pos_x, ultimo_flip, personaje)
                pos_x = valores[0]
                ultimo_flip = valores[1]
                personaje = valores[2]
            elif event.key == pygame.K_LEFT:
                valores = move_left(pos_x, ultimo_flip, personaje)
                pos_x = valores[0]
                ultimo_flip = valores[1]
                personaje = valores[2]
            elif event.key == pygame.K_i:
                idle = not idle
            elif event.key == pygame.K_v:
                voice = True

    #Ejecuta el movimiento automático cada 0.5 segundos:
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_tiempo > 500:
        ultimo_tiempo = tiempo_actual
        if idle:
            valores = move_idle(pos_x, pos_y, ultimo_flip, personaje)
            pos_x = valores[0]
            pos_y = valores[1]
            ultimo_flip = valores[2]
            personaje = valores[3]

    #Ejecuta movimiento por voz:
    if voice:
        valores = move_voice(pos_x, pos_y, ultimo_flip, personaje)
        pos_x = valores[0]
        pos_y = valores[1]
        ultimo_flip = valores[2]
        personaje = valores[3]

    #Render:
    screen.blit(fondo,(0,0))
    screen.blit(personaje,(pos_x,pos_y))
    if idle:
        mensaje = "Movimiento automático activado"
        color_texto = (255, 255, 255)
        opacidad = 128
        color_fondo = (0, 0, 0)
        #Renderiza el texto:
        fuente = pygame.font.SysFont(None, 24)
        texto = fuente.render(mensaje, True, color_texto)
        #Crea cuadro de fondo:
        fondo_texto = pygame.Surface((texto.get_width() + 20, texto.get_height() + 20))
        fondo_texto.set_alpha(opacidad)
        fondo_texto.fill(color_fondo)
        #Centra el texto:
        pos_x_texto = (fondo_texto.get_width() - texto.get_width()) // 2
        pos_y_texto = (fondo_texto.get_height() - texto.get_height()) // 2
        fondo_texto.blit(texto, (pos_x_texto, pos_y_texto))
        screen.blit(fondo_texto, ((800 - fondo_texto.get_width()) // 2, 50))
    pygame.display.update()