"""
Simple example showing some animated shapes
"""
import math
import pyglet
from pyglet import shapes

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()
    cantidad_rectas = 16
    centro_x = window.width / 2
    centro_y = window.height / 2
    r1 = 400
    r2 = 300
    color = (200, 200, 255)
    for i in range(0, cantidad_rectas):
        # Calculamos los cuatro puntos para la siguiente recta.
        angulo1 = i * (2*math.pi/cantidad_rectas)
        angulo2 = (i+1) * (2*math.pi/cantidad_rectas)
        #print(f'Ángulos: <{i},{angulo1},{angulo2}')
        x1 = centro_x + r1*math.cos(angulo1)
        y1 = centro_y + r2*math.sin(angulo1)
        x2 = centro_x + r1*math.cos(angulo2)
        y2 = centro_y + r2*math.sin(angulo2)
        print(f'Puntos=<{i},{x1},{y1},{x2},{y2}')
        #pygame.draw.aaline(screen, (200, 200, 255), (x1, y1), (x2, y2))

        line = shapes.Line(x1, y1, x2, y2, thickness=2, color=color)
        line.draw()


pyglet.app.run()

# class ShapesDemo(pyglet.window.Window):

#     def __init__(self, width, height):
#         super().__init__(width, height, "Óvalo")

#         self.cantidad_rectas = 16
#         self.centro_x = width / 2
#         self.centro_y = height / 2
#         self.r1 = 50
#         self.r2 = 20
#         self.color = (200, 200, 255)
# #        self.batch = pyglet.graphics.Batch()
#         for i in range(0, self.cantidad_rectas):
#             # Calculamos los cuatro puntos para la siguiente recta.
#             angulo1 = i * (2*math.pi/self.cantidad_rectas)
#             angulo2 = (i+1) * (2*math.pi/self.cantidad_rectas)
#             #print(f'Ángulos: <{i},{angulo1},{angulo2}')
#             x1 = self.centro_x + self.r1*math.cos(angulo1)
#             y1 = self.centro_y + self.r2*math.sin(angulo1)
#             x2 = self.centro_x + self.r1*math.cos(angulo2)
#             y2 = self.centro_y + self.r2*math.sin(angulo2)
#             print(f'Puntos=<{i},{x1},{y1},{x2},{y2}')
#             #pygame.draw.aaline(screen, (200, 200, 255), (x1, y1), (x2, y2))

#             self.line = shapes.Line(x1, y1, x2, y2, thickness=2, color=self.color)


#     def on_draw(self):
#         """Clear the screen and draw shapes"""
#         self.clear()
#         self.batch.draw()

#     def update(self, delta_time):
#         """Animate the shapes"""
#         for i in range(0, self.cantidad_rectas):
#             # Calculamos los cuatro puntos para la siguiente recta.
#             angulo1 = i * (2*math.pi/self.cantidad_rectas)
#             angulo2 = (i+1) * (2*math.pi/self.cantidad_rectas)
#             x1 = self.centro_x + self.r1*math.cos(angulo1)
#             y1 = self.centro_y + self.r2*math.sin(angulo1)
#             x2 = self.centro_x + self.r1*math.cos(angulo2)
#             y2 = self.centro_y + self.r2*math.sin(angulo2)
#             print(f'Puntos=<{i},{x1},{y1},{x2},{y2}')
#             #pygame.draw.aaline(screen, (200, 200, 255), (x1, y1), (x2, y2))

#             self.line = shapes.Line(x1, y1, x2, y2, thickness=2, color=self.color)


# if __name__ == "__main__":
#     demo = ShapesDemo(720, 480)
#     pyglet.clock.schedule_interval(demo.update, 1/30)
#     pyglet.app.run()