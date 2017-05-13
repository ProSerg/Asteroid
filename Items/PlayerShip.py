from Asteroid.Items.Unit import Unit
from Asteroid.Items.Astroid import Astroid
import Asteroid.common.Resources as Resources
from Asteroid.common.Point import Point
from Asteroid.common.Figure import *
import math
from pyglet.window import key

class PlayerShip(Unit):
    _loader = None
    player_image = "player_ship.png"

    def __init__(self,
                 fabric,
                 thrust=300,
                 rotate_speed=140,
                 resistance=0.005,
                 rotation=0,
                 *args, **kwargs):
        try:
            super(PlayerShip, self).__init__(
                rotation=rotation,
                user_drive=True,
                static=False,
                img=fabric.fabric_sprite(self.player_image, rotate=0),
                *args, **kwargs)

            self.thrust = thrust
            self.rotate_speed = rotate_speed
            self.resistance = resistance

            self.engine = None
            self._figure = Circle(
                cx=-self.width/6,
                cy=0,
                color=Color.Green,
                radius=self.width/2.3,
                num_segments=20
            )
        except Exception as ex:
            print("PlayerShip: ", ex)

        # self.add_item(self.fire)
        self.key_handler = key.KeyStateHandler()

    def _set_loader(self, loader):
        self._loader = loader

    loader = property(lambda self: self._loader, _set_loader)

    def add_engine(self, fire):
        self.engine = fire
        self.add_item(self.engine)

    def setMoving(self, flag):
        self.fire.visible = flag

    def update(self, dt):
        # Do all the normal physics stuff
        super(PlayerShip, self).update(dt)

        if self.key_handler[key.LEFT]:
            self.velocity_angle = -self.rotate_speed * dt
        elif self.key_handler[key.RIGHT]:
            self.velocity_angle = self.rotate_speed * dt
        else:
            self.velocity_angle = 0
        self.rotation += self.velocity_angle

        angle_radians = -math.radians(self.rotation)
        if self.key_handler[key.UP]:
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            self.velocity_x += force_x
            self.velocity_y += force_y
            # self.fire.rotation = self.rotation - 270
            # self.fire.visible = True
            self.engine.visible = True
        else:
            self.engine.visible = False
        self.velocity_x -= self.velocity_x * self.resistance
        self.velocity_y -= self.velocity_y * self.resistance

    def process(self):
        if self._collision_obj.empty() is True:
            self.figure.color = Color.Green
        else:
            while not self._collision_obj.empty():
                obj = self._collision_obj.get()
                if type(obj) is Astroid:
                    self.figure.color = Color.Red