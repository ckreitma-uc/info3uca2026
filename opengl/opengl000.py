"""
Esqueleto didáctico: mundo 3D con OpenGL (pygame + PyOpenGL)

Objetivo pedagógico:
    - Mostrar un sistema de ejes 3D (X, Y, Z) que se puede rotar con el
      ratón y acercar/alejar (zoom) con la rueda del ratón.
    - Dibujar puntos en el espacio 3D.
    - Calcular "a mano" (con multiplicación de matrices) la proyección
      ortogonal de cada punto sobre los tres planos coordenados
      (XY, XZ, YZ), para entender cómo funcionan las transformaciones.

    Esto es la base para, más adelante, extenderlo a rectas y poliedros.
"""

import math

import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective

# ---------------------------------------------------------------------------
# Configuración de la ventana
# ---------------------------------------------------------------------------
ANCHO_VENTANA = 900
ALTO_VENTANA = 700

# Colores (r, g, b), en el rango 0..1 para OpenGL
BLANCO = (1.0, 1.0, 1.0)
NEGRO = (0.0, 0.0, 0.0)
ROJO = (1.0, 0.2, 0.2)
VERDE = (0.2, 1.0, 0.2)
AZUL = (0.3, 0.5, 1.0)
GRIS = (0.4, 0.4, 0.4)
AMARILLO = (1.0, 1.0, 0.0)
CIAN = (0.2, 1.0, 1.0)
MAGENTA = (1.0, 0.2, 1.0)
BLANCO_HUESO = (1.0, 0.8, 0.6)

LONGITUD_EJES = 5.0

# Normal (unitaria) de un plano de ejemplo que pasa por el origen,
# usado para demostrar la proyección sobre un plano arbitrario.
NORMAL_PLANO_EJEMPLO = np.array([1.0, 1.0, 1.0]) / math.sqrt(3.0)

# Puntos de ejemplo sobre los que se calcularán las proyecciones.
# Se guardan en coordenadas homogéneas (x, y, z, 1) para poder
# multiplicarlos por matrices 4x4.
PUNTOS_3D = [
    np.array([2.0, 3.0, 1.5, 1.0]),
    np.array([-1.5, 2.0, -2.0, 1.0]),
    np.array([1.0, -1.0, 2.5, 1.0]),
]

# ---------------------------------------------------------------------------
# Estado de la cámara (orbital): el usuario gira el mundo con el ratón
# y hace zoom con la rueda.
# ---------------------------------------------------------------------------
camara = {
    "angulo_x": 20.0,   # rotación (pitch) alrededor del eje X, en grados
    "angulo_y": -30.0,  # rotación (yaw) alrededor del eje Y, en grados
    "distancia": 12.0,  # distancia de la cámara al origen (zoom)
}

arrastrando = False
ultima_pos_mouse = (0, 0)


# ---------------------------------------------------------------------------
# Matrices de proyección ortogonal sobre los planos coordenados
# ---------------------------------------------------------------------------
def matriz_proyeccion_xy():
    """Anula la coordenada Z: proyecta el punto sobre el plano XY."""
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1],
    ], dtype=float)


def matriz_proyeccion_xz():
    """Anula la coordenada Y: proyecta el punto sobre el plano XZ."""
    return np.array([
        [1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ], dtype=float)


def matriz_proyeccion_yz():
    """Anula la coordenada X: proyecta el punto sobre el plano YZ."""
    return np.array([
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ], dtype=float)


def matriz_proyeccion_plano(xp, yp, zp):
    """
    Proyección ortogonal sobre el plano que pasa por el origen y cuya
    normal es el vector unitario (xp, yp, zp).

    Cada celda se arma con la fórmula P[i][j] = delta_ij - n_i*n_j, escrita
    término a término (sin recurrir a normal ni a producto externo), ya
    que se asume que (xp, yp, zp) ya es unitario.
    """
    return np.array([
        [1 - xp*xp, -xp*yp, -xp*zp, 0],
        [-xp*yp, 1 - yp*yp, -yp*zp, 0],
        [-xp*zp, -yp*zp, 1 - zp*zp, 0],
        [0, 0, 0, 1],
    ], dtype=float)


def proyectar_punto(punto_homogeneo, matriz):
    """Aplica la transformación (multiplicación matriz @ vector) al punto."""
    return matriz @ punto_homogeneo


# ---------------------------------------------------------------------------
# Dibujo de la escena
# ---------------------------------------------------------------------------
def dibujar_ejes(longitud=LONGITUD_EJES):
    """Dibuja los tres ejes coordenados, cada uno con su color habitual."""
    glLineWidth(2.0)
    glBegin(GL_LINES)

    glColor3f(*ROJO)
    glVertex3f(-longitud, 0, 0)
    glVertex3f(longitud, 0, 0)

    glColor3f(*VERDE)
    glVertex3f(0, -longitud, 0)
    glVertex3f(0, longitud, 0)

    glColor3f(*AZUL)
    glVertex3f(0, 0, -longitud)
    glVertex3f(0, 0, longitud)

    glEnd()


def dibujar_grilla(longitud=LONGITUD_EJES, paso=1.0):
    """Dibuja una grilla tenue sobre el plano XZ, a modo de referencia visual."""
    glColor3f(*GRIS)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    pos = -longitud
    while pos <= longitud:
        glVertex3f(pos, 0, -longitud)
        glVertex3f(pos, 0, longitud)
        glVertex3f(-longitud, 0, pos)
        glVertex3f(longitud, 0, pos)
        pos += paso
    glEnd()


def dibujar_punto(punto_homogeneo, color, tamano=10.0):
    """Dibuja un único punto 3D a partir de sus coordenadas homogéneas."""
    glPointSize(tamano)
    glColor3f(*color)
    glBegin(GL_POINTS)
    glVertex3f(punto_homogeneo[0], punto_homogeneo[1], punto_homogeneo[2])
    glEnd()


def dibujar_linea_punteada(p1, p2, color):
    """Une dos puntos con una línea punteada (para ligar punto y proyección)."""
    glColor3f(*color)
    glLineWidth(1.0)
    glEnable(GL_LINE_STIPPLE)
    glLineStipple(2, 0x0F0F)
    glBegin(GL_LINES)
    glVertex3f(p1[0], p1[1], p1[2])
    glVertex3f(p2[0], p2[1], p2[2])
    glEnd()
    glDisable(GL_LINE_STIPPLE)


def dibujar_puntos_y_proyecciones():
    """
    Por cada punto 3D:
        - lo dibuja en su color (amarillo).
        - calcula sus proyecciones en los planos XY, XZ, YZ multiplicando
          por la matriz de proyección correspondiente.
        - calcula también su proyección sobre un plano arbitrario que pasa
          por el origen (definido por NORMAL_PLANO_EJEMPLO).
        - dibuja cada proyección con un color distinto y una línea
          punteada que la une con el punto original.
    """
    matriz_plano_ejemplo = matriz_proyeccion_plano(*NORMAL_PLANO_EJEMPLO)

    for punto in PUNTOS_3D:
        dibujar_punto(punto, AMARILLO, tamano=12.0)

        proyeccion_xy = proyectar_punto(punto, matriz_proyeccion_xy())
        proyeccion_xz = proyectar_punto(punto, matriz_proyeccion_xz())
        proyeccion_yz = proyectar_punto(punto, matriz_proyeccion_yz())
        proyeccion_plano = proyectar_punto(punto, matriz_plano_ejemplo)

        dibujar_punto(proyeccion_xy, CIAN)
        dibujar_linea_punteada(punto, proyeccion_xy, CIAN)

        dibujar_punto(proyeccion_xz, MAGENTA)
        dibujar_linea_punteada(punto, proyeccion_xz, MAGENTA)

        dibujar_punto(proyeccion_yz, VERDE)
        dibujar_linea_punteada(punto, proyeccion_yz, VERDE)

        dibujar_punto(proyeccion_plano, BLANCO_HUESO)
        dibujar_linea_punteada(punto, proyeccion_plano, BLANCO_HUESO)


# ---------------------------------------------------------------------------
# Configuración inicial de OpenGL
# ---------------------------------------------------------------------------
def configurar_opengl():
    glEnable(GL_DEPTH_TEST)
    glClearColor(*NEGRO, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, ANCHO_VENTANA / ALTO_VENTANA, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def aplicar_camara():
    """
    Ubica la cámara según el estado de rotación (ratón) y zoom (rueda).
    Es un esquema de "cámara orbital": la cámara siempre mira al origen,
    girando alrededor de él.
    """
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -camara["distancia"])
    glRotatef(camara["angulo_x"], 1.0, 0.0, 0.0)
    glRotatef(camara["angulo_y"], 0.0, 1.0, 0.0)


# ---------------------------------------------------------------------------
# Manejo de eventos: rotar con arrastre del ratón, zoom con la rueda
# ---------------------------------------------------------------------------
def procesar_eventos():
    global arrastrando, ultima_pos_mouse

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False

        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # botón izquierdo: iniciar arrastre
                arrastrando = True
                ultima_pos_mouse = evento.pos
            elif evento.button == 4:  # rueda hacia arriba: acercar
                camara["distancia"] = max(2.0, camara["distancia"] - 1.0)
            elif evento.button == 5:  # rueda hacia abajo: alejar
                camara["distancia"] = min(50.0, camara["distancia"] + 1.0)

        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                arrastrando = False

        elif evento.type == pygame.MOUSEMOTION:
            if arrastrando:
                x, y = evento.pos
                dx = x - ultima_pos_mouse[0]
                dy = y - ultima_pos_mouse[1]
                camara["angulo_y"] += dx * 0.4
                camara["angulo_x"] += dy * 0.4
                ultima_pos_mouse = (x, y)

    return True


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    pygame.init()
    pygame.display.set_mode(
        (ANCHO_VENTANA, ALTO_VENTANA),
        pygame.DOUBLEBUF | pygame.OPENGL,
    )
    pygame.display.set_caption("Mundo 3D - Ejes, puntos y proyecciones")

    configurar_opengl()

    reloj = pygame.time.Clock()
    ejecutando = True
    while ejecutando:
        ejecutando = procesar_eventos()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        aplicar_camara()
        dibujar_grilla()
        dibujar_ejes()
        dibujar_puntos_y_proyecciones()

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
