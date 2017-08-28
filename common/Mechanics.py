import math
from pyglet.window import key


class BaseMechanics(object):
    def __init__(self, resistance, rotate_speed, thrust):
        self._resistance = resistance
        self._rotate_speed = rotate_speed
        self._thrust = thrust
        self._rotation = 0
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.velocity_angle = 0.0
        self.dx = 0
        self.dy = 0
        self.da = 0
        self.dt = 0

    def _set_rotate_speed(self, rotate_speed):
        self._rotate_speed = rotate_speed

    def _get_rotate_speed(self):
        return self._rotate_speed

    rotate_speed = property(_get_rotate_speed, _set_rotate_speed)

    def _set_resistance(self, resistance):
        self._resistance = resistance

    def _get_resistance(self):
        return self._resistance

    resistance = property(_get_resistance, _set_resistance)

    def _set_thrust(self, thrust):
        self._thrust = thrust

    def _get_thrust(self):
        return self._thrust

    thrust = property(_get_thrust, _set_thrust)

    def _set_rotation(self, rotation):
        self._rotation = rotation

    def _get_rotation(self):
        return self._rotation

    rotation = property(_get_rotation, _set_rotation)

    def process_live(self):
        pass

    def update(self, dt):
        self.dx = self.velocity_x * dt
        self.dy = self.velocity_y * dt
        pass

    def get_slide(self):
        return self.dx, self.dy, self.da


class AsteroidMechanics(BaseMechanics):
    def __init__(self, resistance, rotate_speed, thrust, live=500):
        super(AsteroidMechanics, self).__init__(
            resistance=resistance,
            rotate_speed=rotate_speed,
            thrust=thrust,
        )
        self.live = live
        self.damage = 0

    def add_damage(self, value):
        self.damage += value

    def process_live(self):
        self.live -= self.damage
        self.damage = 0

    def update(self, dt):
        #self.rotation += self.rotate_speed * dt
        angle_radians = -math.radians(self.rotation)
        self.velocity_x = math.cos(angle_radians) * self.thrust
        self.velocity_y = math.sin(angle_radians) * self.thrust
        self.dx = self.velocity_x * dt
        self.dy = self.velocity_y * dt
        self.da = self.rotate_speed * dt

    def is_live(self):
        return self.live > 0

class BulletMechanics(BaseMechanics):
    def __init__(self, resistance, rotate_speed, thrust, energy=700, damage=200):
        super(BulletMechanics, self).__init__(
            resistance=resistance,
            rotate_speed=rotate_speed,
            thrust=thrust,
        )
        self.boom = False
        self.energy = energy
        self.damage = damage
        self.key_handler = key.KeyStateHandler()

    def destroy(self):
        self.boom = True
        self.energy = -1

    def process_live(self):
        self.energy -= math.sqrt(self.dx ** 2 + self.dy ** 2)

    def update(self, dt):
        angle_radians = -math.radians(self.rotation)
        self.velocity_x = math.cos(angle_radians) * self.thrust
        self.velocity_y = math.sin(angle_radians) * self.thrust
        self.dx = self.velocity_x * dt
        self.dy = self.velocity_y * dt

    def is_live(self):
        return self.energy > 0

class ShipMechanics(BaseMechanics):

    def __init__(self, resistance, rotate_speed, thrust, live=1000):
        super(ShipMechanics, self).__init__(
            resistance=resistance,
            rotate_speed=rotate_speed,
            thrust=thrust,
        )
        self.starting_live = live

        self.live = live
        self.key_handler = key.KeyStateHandler()
        self.damage = 0

    def reset(self):
        self.live = self.starting_live
        self.damage = 0

    def add_damage(self, value):
        self.damage += value

    def process_live(self):
        self.live -= self.damage
        self.damage = 0

    def update(self, dt):

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

        self.velocity_x -= self.velocity_x * self.resistance
        self.velocity_y -= self.velocity_y * self.resistance

        self.dx = self.velocity_x * dt
        self.dy = self.velocity_y * dt
        self.da = self.velocity_angle

    def is_live(self):
        return self.live > 0
