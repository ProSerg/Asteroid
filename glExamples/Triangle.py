import pyglet
import pyglet.gl as gl
from pyglet.graphics import *

from Asteroid.common.Figure import *
from pyglet.window import key

class Triangle(object):
    def __init__(self):
        self.vertices = pyglet.graphics.vertex_list(3,
            ('v2f', [-0.5,-0.5, 0.5,-0.5, 0.0,0.5]),
            # ('v3f', [-0.5,-0.5,0.0, 0.5,-0.5,0.0, 0.0,0.5,0.0]),
            ('c3B', [100,200,220, 200,110,100, 100,250,100]))
        self.vertex_list = pyglet.graphics.vertex_list(1024, 'v3f', 'c4B', 't2f', 'n3f')



class MyWindows(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(MyWindows, self).__init__(*args, **kwargs)
        # self.set_minimum_size(800, 600)
        self.triangle = Triangle()
        self.key_handler = key.KeyStateHandler()
        # self.rectangle = Rectangle(-0.5, -0.5 , 1, 1, [0,200,0])
        # gl.glClearColor(0.2, 0.3, 0.2, 1.0)
        self.push_handlers(self.key_handler)
        self.batch = pyglet.graphics.Batch()
        x = 1.0
        y = 1.0
        x2 = 2.0
# class Rectangle(object):
#     def __init__(self, x1, y1, width, height, color):
#         self.vertices = pyglet.graphics.vertex_list(4,
#             ('v2f', [-0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5]),
            # ('v2f', [
            #     x1, y1,
            #     x1+width, y1,
            #     x1+width, y1+height,
            #     x1, y1+height]),
            # ('c3B', [
            #     color[0], color[1], color[2],
            #     color[0], color[1], color[2],
            #     color[0], color[1], color[2],
            #     color[0], color[1], color[2]]
            #  ))
#
        y2 = 2.0
        width = 1
        height = 1
        self.rotation = 30.0
        self.rotate_speed = 150

        self.rect = Rectangle(
            cx=x - width / 2,
            cy=y - height / 2,
            color=Color.Green,
            width=width,
            height=height,
            rotation=self.rotation
        )

        self.circle = Circle(
            cx=x - width / 2,
            cy=y - height / 2,
            color=Color.Red,
            radius=max(width,height),
            num_segments = 100
        )

        self.circle2 = Circle(
            cx=x2 - width / 2,
            cy=y2 - height / 2,
            color=Color.Red,
            radius=max(width, height),
            num_segments=100
        )

        print(self.rect.points)
        pyglet.clock.schedule_interval(self.update, 1 / 120.0)
        glScalef(0.1, 0.1, 0.1)

    def update(self, dt):
        # print("Update")
        # print(self.rotation)
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
            self.rect.rotate(self.rotation)
        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt
            self.rect.rotate(self.rotation)


    def on_draw(self):
        self.clear()
        self.rect.vertex().draw(GL_LINE_LOOP)
        self.circle.vertex().draw(GL_LINE_LOOP)
        self.circle.vertex().draw(GL_LINE_LOOP)
        self.circle.vertex().draw(GL_LINE_LOOP)
        self.circle2.vertex().draw(GL_LINE_LOOP)

    def on_resize(self, width, height):
        gl.glViewport(0, 0, width, height)




if __name__ == "__main__":
    # windows = MyWindows(width=1280, height=720, caption="My Window" ,resizable=True)
    windows = MyWindows(width=1280, height=720, resizable=True)
    # windows.on_draw()
    pyglet.app.run()