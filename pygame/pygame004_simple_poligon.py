# Ejemplo de Polígono simple a partir de lista de puntos
import pygame



polygon1 = [(50, 50), (200, 50), (200, 200), (50, 200)]

p2 = []
p2.append((300,300))
p2.append((400,400))
p2.append((200,400))




def poligono(canvas, lista_puntos, color):
    puntos = lista_puntos
    inicio = puntos[0]
    puntos.append(inicio)
    print(f'puntos={puntos}')
    p1 = puntos[0]
    linea = 0
    for p2 in puntos[1:]:
        print(f'Linea={linea} p1={p1} p2={p2}')
        pygame.draw.aaline(canvas, color, p1, p2)
        p1 = p2
        linea+=1



# Driver code
if __name__ == '__main__':
    pygame.init()

    color = (20, 20, 20)
    rect_color = (255, 100, 0)

    # CREATING CANVAS
    canvas = pygame.display.set_mode((500, 500))

    # TITLE OF CANVAS
    pygame.display.set_caption("UCA Polígono a partir de lista de puntos")

    exit = False

    while not exit:
        canvas.fill(color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

        poligono(canvas, polygon1, rect_color)
        poligono(canvas, p2, rect_color)
        pygame.display.update()
