# https://openglsamples.sourceforge.net/teapot_py.html
import pygame
from OpenGL.GLU import *
from OpenGL.GL import *

name = 'OpenGL Python Teapot'
quadric = None
angulo_x = 20.0
angulo_y = -30.0
arrastrando = False


def draw_teapot():
    """Dibuja una tetera sencilla usando primitivas GLU."""
    glPushMatrix()
    glScalef(1.4, 1.0, 1.0)
    gluSphere(quadric, 1.5, 32, 16)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 1.35, 0.0)
    gluSphere(quadric, 0.55, 24, 12)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.45, 0.35, 0.0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(quadric, 0.45, 0.12, 1.5, 24, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.25, 0.3, 0.0)
    glRotatef(90, 1, 0, 0)
    glScalef(1.0, 1.0, 0.7)
    gluDisk(quadric, 0.45, 0.75, 24, 8)
    glPopMatrix()


def main():
    global quadric, angulo_x, angulo_y, arrastrando

    pygame.init()
    pygame.display.set_mode((400, 400), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption(name)
    quadric = gluNewQuadric()

    glClearColor(0., 0., 1., 1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [-20., 2., -2., 1.]
    lightZeroColor = [0.7, 1., 0., 1.0]  # green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40., 1., 1., 40.)
    glMatrixMode(GL_MODELVIEW)
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                arrastrando = True
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                arrastrando = False
            elif evento.type == pygame.MOUSEMOTION and arrastrando:
                desplazamiento_x, desplazamiento_y = evento.rel
                angulo_y += desplazamiento_x * 0.5
                angulo_x += desplazamiento_y * 0.5
                angulo_x = max(-89.0, min(89.0, angulo_x))

        display()
        pygame.display.flip()

    gluDeleteQuadric(quadric)
    pygame.quit()


def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 10,
              0, 0, 0,
              0, 1, 0)
    glRotatef(angulo_x, 1, 0, 0)
    glRotatef(angulo_y, 0, 1, 0)
    glPushMatrix()
    color = [1.0, 1., 1., 1.]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
    glRotatef(180, 1, 0, 0)
    glRotatef(-45, 0, 1, 0)
    draw_teapot()

    glPopMatrix()

    return


if __name__ == '__main__':
    main()
