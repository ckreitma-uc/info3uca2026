# https://openglsamples.sourceforge.net/teapot_py.html
from OpenGL import GLUT
from OpenGL import GLU
from OpenGL import GL
import math
import sys

name = 'OpenGL Python Teapot'
camera_yaw = 0.0
camera_pitch = 0.0
camera_distance = 10.0
light_position = [-4.0, 4.0, -4.0, 1.0]
light_color = [1.0, 1.0, 1.0, 1.0]
drag_button = None
last_mouse_position = None


def update_window_title():
    title = (
        'Luz: IJKL/UO | RGB: R/F T/G Y/H | Camara: WASD +/- | '
        'Arrastrar: camara | Rueda: zoom'
    )
    GLUT.glutSetWindowTitle(title)


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def update_view():
    pitch_radians = math.radians(camera_pitch)
    yaw_radians = math.radians(camera_yaw)
    eye_x = camera_distance * math.cos(pitch_radians) * math.sin(yaw_radians)
    eye_y = camera_distance * math.sin(pitch_radians)
    eye_z = camera_distance * math.cos(pitch_radians) * math.cos(yaw_radians)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()
    GLU.gluLookAt(eye_x, eye_y, eye_z, 0, 0, 0, 0, 1, 0)


def change_light_color(component, delta):
    light_color[component] = clamp(light_color[component] + delta, 0.0, 1.0)
    print('RGB de la luz: {:.1f}, {:.1f}, {:.1f}'.format(*light_color[:3]))


def keyboard(key, x, y):
    global camera_yaw, camera_pitch, camera_distance

    key = key.decode('utf-8').lower()
    step = 0.2
    if key == '\x1b':
        sys.exit()
    elif key == 'w':
        camera_pitch = clamp(camera_pitch + 3.0, -85.0, 85.0)
    elif key == 's':
        camera_pitch = clamp(camera_pitch - 3.0, -85.0, 85.0)
    elif key == 'a':
        camera_yaw -= 3.0
    elif key == 'd':
        camera_yaw += 3.0
    elif key in ('+', '='):
        camera_distance = clamp(camera_distance - 0.5, 3.0, 30.0)
    elif key == '-':
        camera_distance = clamp(camera_distance + 0.5, 3.0, 30.0)
    elif key == 'i':
        light_position[1] += step
    elif key == 'k':
        light_position[1] -= step
    elif key == 'j':
        light_position[0] -= step
    elif key == 'l':
        light_position[0] += step
    elif key == 'u':
        light_position[2] -= step
    elif key == 'o':
        light_position[2] += step
    elif key == 'r':
        change_light_color(0, 0.1)
    elif key == 'f':
        change_light_color(0, -0.1)
    elif key == 't':
        change_light_color(1, 0.1)
    elif key == 'g':
        change_light_color(1, -0.1)
    elif key == 'y':
        change_light_color(2, 0.1)
    elif key == 'h':
        change_light_color(2, -0.1)
    GLUT.glutPostRedisplay()


def mouse(button, state, x, y):
    global camera_distance, drag_button, last_mouse_position

    if button == 3 and state == GLUT.GLUT_DOWN:
        camera_distance = clamp(camera_distance - 0.5, 3.0, 30.0)
    elif button == 4 and state == GLUT.GLUT_DOWN:
        camera_distance = clamp(camera_distance + 0.5, 3.0, 30.0)
    elif button == GLUT.GLUT_LEFT_BUTTON:
        drag_button = button if state == GLUT.GLUT_DOWN else None
        last_mouse_position = (x, y) if state == GLUT.GLUT_DOWN else None
    GLUT.glutPostRedisplay()


def mouse_motion(x, y):
    global camera_yaw, camera_pitch, last_mouse_position

    if drag_button != GLUT.GLUT_LEFT_BUTTON or last_mouse_position is None:
        return
    previous_x, previous_y = last_mouse_position
    camera_yaw += (x - previous_x) * 0.4
    camera_pitch = clamp(camera_pitch - (y - previous_y) * 0.4, -85.0, 85.0)
    last_mouse_position = (x, y)
    GLUT.glutPostRedisplay()


def main():
    GLUT.glutInit(sys.argv)
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
    GLUT.glutInitWindowSize(800, 800)
    GLUT.glutCreateWindow(name)

    GL.glClearColor(0., 0., 1., 1.)
    GL.glShadeModel(GL.GL_SMOOTH)
    GL.glEnable(GL.GL_CULL_FACE)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_LIGHTING)
    GL.glLightf(GL.GL_LIGHT0, GL.GL_CONSTANT_ATTENUATION, 0.1)
    GL.glLightf(GL.GL_LIGHT0, GL.GL_LINEAR_ATTENUATION, 0.05)
    GL.glEnable(GL.GL_LIGHT0)
    GLUT.glutDisplayFunc(display)
    GLUT.glutKeyboardFunc(keyboard)
    GLUT.glutMouseFunc(mouse)
    GLUT.glutMotionFunc(mouse_motion)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GLU.gluPerspective(40., 1., 1., 40.)
    update_window_title()
    print('Controles: IJKL/UO luz, R/F T/G Y/H RGB, WASD camara, +/- o rueda zoom.')
    GLUT.glutMainLoop()
    return


def display():

    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    update_view()
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, light_color)

    GL.glPushMatrix()
    GL.glTranslatef(*light_position[:3])
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, light_color)
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, light_color)
    GLUT.glutSolidSphere(0.18, 20, 20)
    GL.glPopMatrix()

    GL.glPushMatrix()
    color = [1.0, 1., 1., 1.]
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, color)
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
    # GL.glRotatef(180, 1, 0, 0)
    # GL.glRotatef(-45, 0, 1, 0)
    GLUT.glutSolidTeapot(1, 1, 1)

    GL.glPopMatrix()
    # GL.glFlush()
    GLUT.glutSwapBuffers()

    return


if __name__ == '__main__':
    main()
