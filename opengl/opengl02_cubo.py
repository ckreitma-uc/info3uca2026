import pygame
from OpenGL import GL
from OpenGL import GLU

altura, ancho = 600, 600
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)


def Cube():
    # Borrar la pantalla
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    # Selecciona la matriz de proyección
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()  # Inicializar la matriz.

    # Ángulo, ratio, near, far
    GLU.gluPerspective(45, altura/ancho, 0.1, 100.0)

    # Seleccionar la matriz modelview
    GL.glMatrixMode(GL.GL_MODELVIEW)

    # Inicializar la matriz.
    GL.glLoadIdentity()

    GL.glTranslatef(0.0, 0.0, -20)

    # Ángulo,
    #GL.glRotatef(45, 0, 0, 1)
    GL.glBegin(GL.GL_LINES)
    for edge in edges:
        for vertex in edge:
            GL.glVertex3fv(vertices[vertex])
    GL.glEnd()
    GL.glFlush()


def main():
    pygame.init()
    pygame.display.set_mode((altura, ancho), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("Cubo 3D sencillo con lineas")

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False

        Cube()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
