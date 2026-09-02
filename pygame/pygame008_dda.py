import pygame

# Ancho y alto teórico
ancho_teorico = 600
alto_teorico = 600

# Ancho y alto real
ancho_real = 70
alto_real = 70

# Relation (ratio) de aspecto entre el real y el teórico
delta_x = int(ancho_teorico/ancho_real)
delta_y = int(alto_teorico/alto_real)

screen = pygame.display.set_mode((ancho_teorico, alto_teorico))
running = True

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRIS = (80, 80, 80)
ROJO = (255, 10, 10)
YELLOW = (255, 255, 0)


def dibujar_grilla(screen):

    # Líneas horizontales
    for pos_y in range(0, alto_teorico, delta_y):
        # print(f'pos_y={pos_y}')
        pygame.draw.aaline(screen, GRIS, (0, pos_y), (ancho_teorico, pos_y))

    # Líneas verticales
    for pos_x in range(0, ancho_teorico, delta_x):
        # print(f'pos_y={pos_y}')
        pygame.draw.aaline(screen, GRIS, (pos_x, 0), (pos_x, alto_teorico))


def pixel(screen, x, y, color):
    x = int(x)
    y = int(y)
    if x < 0 or x > ancho_real or y < 0 or y > alto_real:
        print(f'Punto incorrecto <{x},{y}>')
        return
    pixel_real = (x*delta_x, (alto_real-y)*delta_y, delta_x, delta_y)
    print(f'Pixel real={pixel_real}')
    # Rectángulo (<origen>,<ancho>,<alto>)
    pygame.draw.rect(screen, color, pixel_real)

def linea_dda(screen, x0, y0, x1, y1, color):
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        pixel(screen, x0, y0, color)
        return
    x_inc = dx / steps
    y_inc = dy / steps
    x = x0
    y = y0
    for _ in range(steps + 1): 
        pixel(screen, round(x), round(y), color) # Operación costosa
        x += x_inc
        y += y_inc



while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False
    screen.fill(BLACK)
    x0,y0,x1,y1 = 30,2,50,37
    pygame.draw.aaline(screen, ROJO, (int(x0*delta_x), (alto_real-y0)*delta_y), (x1*delta_x, (alto_real-y1)*delta_y), 2)
    dibujar_grilla(screen)
    # Dibujar línea usando DDA
    linea_dda(screen, x0, y0, x1, y1, YELLOW)
    punto1 = (4, 17)
    #pixel(screen, punto1[0], punto1[1], WHITE)
    pygame.display.flip()