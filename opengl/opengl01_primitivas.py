# https://pharos.sh/breve-introduccion-a-opengl-en-python-con-pyopengl/

from OpenGL import GL
import pygame
# from OpenGL.GLU import *


w, h = 500, 500


def square():
    GL.glColor3f(1.0, 0.8, 0.6)
    GL.glBegin(GL.GL_QUADS)
    GL.glVertex2f(100, 100)
    GL.glVertex2f(200, 100)
    GL.glVertex2f(200, 200)
    GL.glVertex2f(100, 200)
    GL.glEnd()


def triangulo1():
    GL.glColor3f(0.5, 0.9, 0.1)
    GL.glBegin(GL.GL_TRIANGLES)
    GL.glVertex2f(400, 50)
    GL.glVertex2f(300, 200)
    GL.glVertex2f(250, 100)
    GL.glVertex2f(50, 400)
    GL.glVertex2f(80, 430)
    GL.glVertex2f(70, 400)
    GL.glEnd()


def cuadrilatero2():
    GL.glColor3f(0.80, 0.5, 0.9)
    GL.glBegin(GL.GL_QUADS)
    GL.glVertex2f(150, 250)
    GL.glVertex2f(450, 300)
    GL.glVertex2f(350, 350)
    GL.glVertex2f(150, 300)
    GL.glEnd()


def iterate():
    GL.glViewport(0, 0, 500, 500)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(0.0, 500, 0.0, 500, 0.0, 2.0)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()


def showScreen():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()
    iterate()
    square()
    cuadrilatero2()
    triangulo1()


def main():
    pygame.init()
    pygame.display.set_mode((w, h), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("Primitivas")

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False

        showScreen()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
