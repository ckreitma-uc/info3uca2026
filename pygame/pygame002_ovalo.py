import pygame
from math import sin, cos, pi
from time import sleep
ancho = 800
alto = 800
screen = pygame.display.set_mode((ancho, alto))
running = True

centro = {
    'x': ancho/2,
    'y': alto/2
}

r1 = 350
r2 = 150

cantidad_rectas = 16
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False
    screen.fill((0, 0, 0))
    for i in range(0, cantidad_rectas):
        # Calculamos los cuatro puntos para la siguiente recta.
        angulo1 = i * (2*pi/cantidad_rectas)
        angulo2 = (i+1) * (2*pi/cantidad_rectas)
        #print(f'Ángulos: <{i},{angulo1},{angulo2}')
        x1 = centro['x'] + r1*cos(angulo1)
        y1 = centro['y'] + r2*sin(angulo1)
        x2 = centro['x'] + r1*cos(angulo2)
        y2 = centro['y'] + r2*sin(angulo2)
        # print(f'Puntos=<{i},{x1},{y1},{x2},{y2}')
        pygame.draw.aaline(screen, (200, 200, 255), (x1, y1), (x2, y2))

    pygame.display.flip()