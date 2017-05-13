from Asteroid.Items.Unit import Unit
import Asteroid.common.Resources as Resources
from Asteroid.common.Figure import *

class Astroid(Unit):
    asteroid_image = "asteroid_brown.png"

    def __init__(self, thrust=400, rotate_speed=140, angle_moving=60,  *args, **kwargs):
        super(Astroid, self).__init__(
            thrust=thrust,
            rotate_speed=rotate_speed,
            resistance=0.000,
            static=False,
            img=Resources.make_image(name_file=self.asteroid_image),
            *args, **kwargs)
        self._k = 12

        self._figure = Circle(
            cx=0,
            cy=0,
            color=Color.Red,
            radius=self.width/2,
            num_segments=20
        )
        self._angle_moving = angle_moving

    def update(self, dt):
        super(Astroid, self).update(dt)
        self.rotation -= self.rotate_speed * dt
        angle_radians = -math.radians(self._angle_moving)
        self.velocity_x = math.cos(angle_radians) * self.thrust * dt * self._k
        self.velocity_y = math.sin(angle_radians) * self.thrust * dt * self._k