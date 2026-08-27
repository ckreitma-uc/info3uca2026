import pygame
import time
import numpy as np
ancho = 1200
alto = 900

BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
ROJO = (255, 10, 10)


def rellenar(screen, puntos, color_fuera=ROJO, color_dentro=BLANCO):
    p = np.array(puntos)
    miny, maxy = p[:, 1].min(), p[:, 1].max()
    for pos_y in range(miny, maxy):
        escanear_linea_counting(screen, puntos, pos_y=pos_y, color_dentro=color_dentro, color_fuera=color_fuera)



# ===================================================================

# cn_PnPoly(): crossing number test for a point in a polygon
#     Input:  P = a point,
#             V[] = vertex points of a polygon
#     Return: 0 = outside, 1 = inside
# This code is patterned after [Franklin, 2000]


def cn_PnPoly(P, V):
    cn = 0    # the crossing number counter

    # repeat the first vertex at end
    V = tuple(V[:])+(V[0],)

    # loop through all edges of the polygon
    for i in range(len(V)-1):   # edge from V[i] to V[i+1]
        if ((V[i][1] <= P[1] and V[i+1][1] > P[1])   # an upward crossing
                or (V[i][1] > P[1] and V[i+1][1] <= P[1])):  # a downward crossing
            # compute the actual edge-ray intersect x-coordinate
            vt = (P[1] - V[i][1]) / float(V[i+1][1] - V[i][1])
            if P[0] < V[i][0] + vt * (V[i+1][0] - V[i][0]):  # P[0] < intersect
                cn += 1  # a valid crossing of y=P[1] right of P[0]

    return cn % 2   # 0 if even (out), and 1 if odd (in)


def escanear_linea_counting(screen, puntos, pos_y, color_fuera=ROJO, color_dentro=BLANCO):
    """Dibuja una línea en el screen a la altura "pos_y"
    Args:
        screen ([type]): [description]
        puntos (lista de puntos): lista de puntos
    """
    # Primero vamos a encontrar el menor y el mayor de las x e y para no barrer toda la pantalla.
    p = np.array(puntos)
    minx, maxx, miny, maxy = p[:, 0].min(), p[:, 0].max(), p[:, 1].min(), p[:, 1].max()
    #print(f'Los puntos extremos son: {minx} {maxx} {miny} {maxy}')

    # En el caso de que la altura no esté en el rango retornamos
    if pos_y < miny or pos_y > maxy:
        return

    # Nos posicionamos a la altura indicada y hacemos un ciclo para las x
    color = color_fuera
    # Nos movemos horizontalmente
    for x in range(minx-1, maxx+1):
        cn = cn_PnPoly((x, pos_y), puntos)
        #print(f'wn para ({x},{pos_y})={wn}')
        if (cn % 2) == 0:
            #print(f'Cruce pares para x={x} pos_y={pos_y} anteriores:{lados_anteriores} lados actuales={lados_actuales}')
            color = color_fuera
        else:
            #print(f'Cruce impares para x={x} pos_y={pos_y} anteriores:{lados_anteriores} lados actuales={lados_actuales}')
            color = color_dentro
        pygame.draw.aaline(screen, color, (x, pos_y), (x, pos_y))


def leer_puntos(archivo='./pygame/poligono1.txt'):
    # Toma el archivo y crea una lista de puntos.
    puntos = []
    datos = open(archivo)
    try:
        for linea in datos:
            x, y = linea.split(',')
            #print(f'linea={linea} {x} {y}')
            puntos.append((int(x), int(y)))
    except:
        print(f'Error al abrir el archivo {archivo}')
    finally:
        datos.close()
    return puntos

# Dibuja los bordes partiendo de una lista de puntos.


def dibujar_bordes(screen, puntos, color=AZUL):
    for i in range(0, len(puntos)-1):
        pygame.draw.aaline(screen, color, puntos[i], puntos[i+1])


def principal():
    screen = pygame.display.set_mode((ancho, alto))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False        
        screen.fill((0, 0, 0))
        archivo = './pygame/dino.txt'
        dibujar_bordes(screen, leer_puntos(archivo))
        rellenar(screen, leer_puntos(archivo))
        pygame.display.flip()
        # time.sleep(3)


if __name__ == '__main__':

    # Simulamos un escaneo
    #punto0 = (2, 1)
    #punto1 = (-1, -5)
    #y = -2
    # for x in range(-4, 6):
    #    print(f'Recta en {x}={valor_y(punto0,punto1,x)}')
    #    punto = (int(x), int(y))
    #    print(f'Lado: {punto0},{punto1},{punto} Lado={encontrar_lado(punto0,punto1,punto)}')

    #escanear_linea('hola', leer_puntos(), pos_y=200)
    principal()