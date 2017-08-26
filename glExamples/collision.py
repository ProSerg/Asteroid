import pyglet
from pyglet.window import key
from Asteroid.common.Figure import *
from pyglet.graphics import *
from Asteroid.Items.ItemObject import ItemObject
from Asteroid.Items.ItemObject import ItemObject
from Asteroid.UserUI import UserUI
from Asteroid.common.Resources import *
from Asteroid.common.Figure import *
from Asteroid.common.Mechanics import *

import pyglet.gl as gl



def isCircleToRect(cx, cy, radius, rx, ry, width, height):
    x = cx
    y = cy

    if cx < rx:
        x = rx
    elif cx > (rx + width):
        x = rx + width

    if cy < ry:
        y = ry
    elif cy > (ry + height):
        y = ry + height

    return ((cx - x) * (cx - x) + (cy - y) * (cy - y)) <= (radius * radius)


class Color(Enum):
    White = [255,255,255]
    Red = [255,0,0]
    Lime = [ 0,255,0]
    Blue = [0,0,255]
    Yellow = [255,255,0]
    Aqua = [0,255,255]
    Magenta = [255,0,255]
    Silver = [192,192,192]
    Gray = [128,128,128]
    Maroon = [128,0,0]
    Olive = [128,128,0]
    Green = [0,128,0]
    Purple = [128,0,128]
    Teal = [0,128,128]
    Navy = [0,0,128]

class Line(object):
    def __init__(self, x1, y1 , x2, y2, color):
        self._color = color
        self.num_segments = 2
        self.points = [x1,y1,x2,y2]
        self.colors = []
        for idx in range(self.num_segments):
            for color in self._color.value:
                self.colors.append(color)
        self.vertex = pyglet.graphics.vertex_list(self.num_segments,
            ('v2f', self.points),
            ('c3B', self.colors))



class MyWindows(pyglet.window.Window):

    def __init__(self, scale=0.005, gx0=0, gy0=0, *args, **kwargs):
        super(MyWindows, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.loader = ResourcesLoader(path_to_resource="../../resources")
        self.fabric = Fabric(self.loader, self.batch)

        self.key_handler = key.KeyStateHandler()
        self.push_handlers(self.key_handler)
        self.dt = 1 / 120.0
        self.rotate_speed = 140
        self.velocity_angle = 0.0
        pyglet.clock.schedule_interval(self.update, self.dt)
        self.circle = Circle(
            radius=1, color=Color.Red , num_segments=100,
            slide_x=0, slide_y=0)


        sprite = self.fabric.get_sprite(
            name="mine.png",
            scale=0.4,
            rotation=90,
        )

        self.mine = ItemObject(
            x=200,
            y=300,
            name="mine",
            sprite=sprite,
            bounds=Circle(radius=sprite.width/2,  color=Color.Blue),
        )

        sprite = self.fabric.get_sprite(
            name="player_ship.png",
            scale=0.1,
            rotation=90,
        )

        self.ship = ItemObject(
            x=200,
            y=200,
            name="UserShip",
            sprite=sprite,
            bounds=Rectangle(width=sprite.width, height=sprite.height, rotation=0, color=Color.Green),
        )

        self.obj = []

        self.obj.append(self.ship)
        self.obj.append(self.mine)

        self.draged = None

    def contains(self, x, y):
        """Return true if a point is inside the rectangle."""
        for obj in self.obj:
            if obj.bounds.contains(x,y) is True:
                return obj
        return None

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        # if symbol == pyglet.window.key.LEFT:
        #     self.ship.move(da=-self.rotate_speed * self.dt)
        # if symbol == pyglet.window.key.RIGHT:
        #     self.ship.move(da=self.rotate_speed * self.dt)
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        print("press ", x, y)
        print("contaions: ", self.contains(x, y) )
        self.draged = self.contains(x, y)


    def on_mouse_release(self, x, y, button, modifiers):
        self.draged = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.draged:
            self.draged.move(dx,dy)

    def update(self, dt):
        velocity_angle = 0.0
        if self.key_handler[key.LEFT]:
            velocity_angle = -self.rotate_speed * dt
        elif self.key_handler[key.RIGHT]:
            velocity_angle = self.rotate_speed * dt

        self.ship.move(da=velocity_angle)
        self.collitions()

    def collitions(self):
        # print("Ship ", self.ship.x, self.ship.y, self.ship.bounds.height, self.ship.bounds.width )
        # print("Mine ", self.mine.x, self.mine.y, self.mine.bounds.radius)
        rx = self.ship.x - self.ship.bounds.width/2
        ry = self.ship.y - self.ship.bounds.height/2
        width = self.ship.bounds.width
        height = self.ship.bounds.height
        cx = self.mine.x
        cy = self.mine.y
        radius = self.mine.bounds.radius
        if isCircleToRect(cx, cy, radius, rx, ry, width, height):
            self.ship.bounds.color = Color.Red
        else:
            self.ship.bounds.color = Color.Green

    def projection(self, obj):
        """

        :param obj:  объект типа figure
        :return:
        """
        line_x = None
        line_y = None
        if type(obj) is Rectangle:
            line_y = Line(x1=60, y1=obj.bottom(), x2=60, y2=obj.top(), color=Color.Red)
            line_x = Line(x1=obj.left(), y1=60, x2=obj.right(), y2=60, color=Color.Red)

        if type(obj) is Circle:
            line_y = Line(x1=65, y1=obj.bottom(), x2=65, y2=obj.top(), color=Color.White)
            line_x = Line(x1=obj.left(), y1=65, x2=obj.right(), y2=65, color=Color.White)

        return (line_x , line_y)

    def on_draw(self):
        self.clear()
        line_x = Line(x1=-50, y1=50, x2=500, y2=50, color=Color.Teal)
        line_x.vertex.draw(GL_LINE_LOOP)
        line_y = Line(x1=50, y1=-50, x2=50, y2=500, color=Color.Teal)
        line_y.vertex.draw(GL_LINE_LOOP)
        self.circle.vertex().draw(GL_LINE_LOOP)
        # self.ship.draw()

        for obj in self.obj:
            obj.draw()

        for obj in self.obj:
            lx, ly = self.projection(obj.bounds)
            lx.vertex.draw(GL_LINE_LOOP)
            ly.vertex.draw(GL_LINE_LOOP)

    #def on_resize(self, width, height):
    #    gl.glViewport(0, 0, width, height)





if __name__ == "__main__":
    # windows = MyWindows(width=1280, height=720, caption="My Window" ,resizable=True)
    windows = MyWindows(width=800, height=600, )#resizable=True)
    pyglet.app.run()