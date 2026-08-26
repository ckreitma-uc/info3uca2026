# Ejemplo de Polígono simple a partir de lista de puntos de archivo
import pygame


def leer_puntos(archivo='./pygame/dino.txt'):
    # Toma el archivo y crea una lista de puntos.
    puntos = []
    datos = open(archivo)
    try:
        for linea in datos:
            x, y = linea.split(',')
            puntos.append((int(x), int(y)))
    except:
        print(f'Error al abrir el archivo {archivo}')
    finally:
        datos.close()
    return puntos


def poligono(canvas, lista_puntos, color):
    puntos = lista_puntos
    p1 = puntos[0]
    linea = 0
    for p2 in puntos[1:]:
        print(f'Linea={linea} p1={p1} p2={p2}')
        pygame.draw.aaline(canvas, (200, 200, 255), p1, p2)
        p1 = p2
        linea += 1


# Driver code
if __name__ == '__main__':
    pygame.init()

    color = (20, 20, 20)
    rect_color = (255, 100, 0)

    # CREATING CANVAS
    canvas = pygame.display.set_mode((600, 600))

    # TITLE OF CANVAS
    pygame.display.set_caption("POLIGONO")

    exit = False

    while not exit:
        canvas.fill(color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

        poligono(canvas, leer_puntos(archivo='./pygame/dino.txt'), rect_color)
        # pygame.draw.rect(canvas, rect_color, pygame.Rect(30, 30, 60, 60))
        pygame.display.update()
