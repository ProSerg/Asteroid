
import random
from Asteroid.common.Resources import *
from Asteroid.common.Figure import *
from Asteroid.common.Mechanics import *
from Asteroid.common.AnimationManager import *
from Asteroid.common.UnitManager import *


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

    def __init__(self, loader, scale=0.005, gx0=0, gy0=0, *args, **kwargs):
        super(MyWindows, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.group_effects = pyglet.graphics.OrderedGroup(1)
        self.group_units = pyglet.graphics.OrderedGroup(0)

        self.loader = loader
        self.unit_manager = UnitManager(self.loader, self.batch)
        self.anim_manager = AnimationManager(loader=self.loader, batch=self.batch)
        self.key_handler = key.KeyStateHandler()
        self.push_handlers(self.key_handler)

        self.dt = 1 / 120.0
        self.rotate_speed = 140
        self.velocity_angle = 0.0
        pyglet.clock.schedule_interval(self.update, self.dt)


    def init(self):
        self.anim_manager.createSpringEffect(
            name="greenboom",
            img="_LPE__Elemental_Burst_by_LexusX2.png",
            scale=.8, type_image="grid", duration=0.03, rotation=0.0, rows=6, columns=5)

        self.obj = []

        for i in range(10):
            sprite = self.unit_manager.get_sprite(
                name="mine.png",
                group=self.group_units,
                scale=0.3,
                rotation=90,
            )

            item = ItemObject(
                x=random.randint(100, 350),
                y=random.randint(100, 350),
                name="mine{}".format(i),
                sprite=sprite,
                bounds=Circle(radius=sprite.width/2,  color=Color.Blue),
            )
            self.obj.append(item)

        for i in range(10):
            sprite = self.unit_manager.get_sprite(
                name="asteroid_brown.png",
                group=self.group_units,
                scale=0.1,
                rotation=90,
            )

            item = ItemObject(
                x=random.randint(350,550),
                y=random.randint(350,550),
                name="asteroid{}".format(i),
                sprite=sprite,
                bounds=Circle(radius=sprite.width/2,  color=Color.Blue),
            )
            self.obj.append(item)


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
        self.unit = self.contains(x, y)
        if self.unit:
            self.destroy(self.unit)

    def on_mouse_release(self, x, y, button, modifiers):
        self.draged = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.draged:
            self.draged.move(dx,dy)

    def destroy(self, unit):
        print("unit: ", unit.name)
        self.anim_manager.playAnimation("greenboom", unit.x, unit.y, unit.rotation, self.group_effects)
        self.obj.remove(unit)
        unit.destroy()


    def update(self, dt):
        velocity_angle = 0.0
        if self.key_handler[key.LEFT]:
            velocity_angle = -self.rotate_speed * dt
        elif self.key_handler[key.RIGHT]:
            velocity_angle = self.rotate_speed * dt


    def on_draw(self):
        self.clear()
        self.batch.draw()




if __name__ == "__main__":
    path_to_resource = "../../resources/"
    resource_paths = [
        "".join((path_to_resource, "/Blue")),
        "".join((path_to_resource, "/Effects/Blue Effects")),
        "".join((path_to_resource, "/Effects/Galaxy")),
        "".join((path_to_resource, "/Effects/Grids")),
        "".join((path_to_resource, "/Effects/Proton Star")),
        "".join((path_to_resource, "/Effects/Red Explosion")),
        "".join((path_to_resource, "/Effects/Fires")),
    ]
    loader = ResourcesLoader(resource_paths)
    windows = MyWindows(loader=loader, width=800, height=600)
    windows.init()
    pyglet.app.run()