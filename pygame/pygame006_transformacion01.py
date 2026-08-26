# Ejemplo de Polígono simple a partir de lista de puntos
import pygame
import numpy as np
import math


def poligono(canvas, lista_puntos, color):
    puntos = lista_puntos
    p1 = puntos[0]
    linea = 0
    for p2 in puntos[1:]:
        # print(f'Linea={linea} p1={p1} p2={p2}')
        pygame.draw.line(canvas, color, (p1[0], p1[1]), (p2[0], p2[1]), 5)
        p1 = p2
        linea += 1


def transformar(lista_puntos, matriz):
    homogenea = []
    for p in lista_puntos:
        homogenea.append((p[0], p[1], 1))

    transformada = np.matmul(homogenea, matriz)
    print(f'matriz={matriz}')
    return transformada


# Driver code
if __name__ == '__main__':
    pygame.init()

    color = (20, 20, 20)
    rect_color = (255, 100, 0)

    # CREATING CANVAS
    canvas = pygame.display.set_mode((600, 600))

    # TITLE OF CANVAS
    pygame.display.set_caption("UCA Transformaciones")

    exit = False
    lista_puntos = ((30, 60), (250, 250), (100, 300), (150, 200), (30, 60))

    # Matriz de escala
    escalar = [[3.3, 0, 0],
               [0, 1.3, 0],
               [0, 0, 1]
               ]

    lista_puntos1 = transformar(lista_puntos, escalar)

    # Matriz de rotación
    angulo = -0.40
    rotacion = [[math.cos(angulo), math.sin(angulo), 0],
                [-1*math.sin(angulo), math.cos(angulo), 0],
                [0, 0, 1]]

    lista_puntos2 = transformar(lista_puntos, rotacion)

    # Matriz de traslación.
    traslacion = [[1, 0, 0],
                  [0, 1, 0],
                  [200, 10, 1]]
    lista_puntos3 = transformar(lista_puntos, traslacion)

    # Combinacion.
    xc = 150
    yc = 180
    fi = 0.6

    trasladar_al_origen = [[1, 0, 0],
                            [0, 1, 0],
                            [-1*xc, -1*yc, 1]]

    rotacion_fi = [[math.cos(fi), math.sin(fi), 0],
                   [-1*math.sin(fi), math.cos(fi), 0],
                   [0, 0, 1]]

    destraslacion = [[1, 0, 0],
                     [0, 1, 0],
                     [xc, yc, 1]]
    
    m = np.matmul(np.matmul(trasladar_al_origen, rotacion_fi), destraslacion)
    lista_puntos5 = transformar(lista_puntos, m)

    traslacion2 = [[1, 0, 0],
                   [0, 1, 0],
                   [300, 100, 1]]
    
    lista_puntos4 = transformar(lista_puntos, np.matmul(np.matmul(np.matmul(rotacion, rotacion), escalar), traslacion2))

    while not exit:
        canvas.fill(color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

        poligono(canvas, lista_puntos, rect_color)
        #poligono(canvas, lista_puntos1, (200, 120, 100))
        # poligono(canvas, lista_puntos2, (100, 150, 40))
        # poligono(canvas, lista_puntos3, (50, 200, 200))
        # poligono(canvas, lista_puntos4, (150, 30, 200))
        poligono(canvas, lista_puntos5, (240, 20, 50))
        pygame.display.update()
