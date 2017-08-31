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

    def process_live(self, dt):
        pass

    def update(self, dt):
        self.dx = self.velocity_x * dt
        self.dy = self.velocity_y * dt
        pass

    def get_slide(self):
        return self.dx, self.dy, self.da


class AsteroidMechanics(BaseMechanics):
    def __init__(self, resistance, rotate_speed, typeAsteroid, thrust, live=500):
        super(AsteroidMechanics, self).__init__(
            resistance=resistance,
            rotate_speed=rotate_speed,
            thrust=thrust,
        )
        self.live = live
        self.damage = 0
        self.typeAsteroid = typeAsteroid

    def add_damage(self, value):
        self.damage += value

    def process_live(self, dt):
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

    def process_live(self, dt):
        self.energy -= math.sqrt(self.dx ** 2 + self.dy ** 2)

    def update(self, dt):
        angle_radians = -math.radians(self.rotation)
        self.velocity_x = math.cos(angle_radians) * self.thrust
        self.velocity_y = math.sin(angle_radians) * self.thrust
        self.dx = self.velocity_x * dt
        self.dy = self.velocity_y * dt

    def is_live(self):
        return self.energy > 0

class StarMechanics(BaseMechanics):
    def __init__(self, cost, time):
        super(StarMechanics, self).__init__(
            resistance=0,
            rotate_speed=0,
            thrust=0,
        )
        self.cost = cost
        self.time = time
        self.ctime = 0
        self.live = True
        self.boom = False

    def destroy(self):
        self.live = False

    def process_live(self, dt):
        if self.ctime > self.time:
            self.live = False
            self.boom = True
        else:
            self.ctime += dt

    def is_live(self):
        return self.live

class ShipMechanics(BaseMechanics):

    def __init__(self, resistance, rotate_speed, thrust,  magazine=3, live=1000):
        super(ShipMechanics, self).__init__(
            resistance=resistance,
            rotate_speed=rotate_speed,
            thrust=thrust,
        )
        self._time_reload_weapon = 0
        self._const_reload_weapon_time = 2

        self._time_reload_engine = 0
        self._const_reload_engine_time = 3

        self.magazine = magazine
        self.charge = self.magazine
        self.starting_live = live
        self._cost_bullet = 1.0
        self._reload_power = 1.8
        self._reload_energy = 15.0
        self._cost_energy = 30.0
        self.live = live
        self.key_handler = key.KeyStateHandler()
        self.damage = 0
        self.max_energy = 200
        self.energy = self.max_energy
        self._moving = False

    def getAmmo(self):
        ammo = (self.charge/self.magazine) * 100
        if ammo > 100:
            ammo = 100
        return int(ammo)

    def getLive(self):
        live = (self.live / float(self.starting_live)) * 100
        if live > 100:
            live = 100
        return int(live)

    def getEnergy(self):
        energy = (self.energy / float(self.max_energy))
        if energy > 1.0:
            energy = 1.0
        return energy

    def reset(self):
        self.live = self.starting_live
        self.charge = self.magazine
        self.energy = self.max_energy
        self.damage = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_angle = 0

    def add_damage(self, value):
        self.damage += value

    def expens_energy(self, value):
        self.energy -= value

    def shoot(self):
        if self.charge > self._cost_bullet:
            self.charge -= self._cost_bullet
            self._time_reload_weapon = self._const_reload_weapon_time
            return True
        return False

    def process_live(self, dt):
        self.live -= self.damage
        self.damage = 0

    def update(self, dt):
        force_x = 0
        force_y = 0
        if self.key_handler[key.LEFT]:
            if self.energy < self._cost_energy:
                self.velocity_angle = -self.rotate_speed * dt * 0.5
            else:
                self.velocity_angle = -self.rotate_speed * dt
                # self.expens_energy(dt*self._cost_energy*0.2)
        elif self.key_handler[key.RIGHT]:
            if self.energy < self._cost_energy :
                self.velocity_angle = self.rotate_speed * dt * 0.5
            else:
                self.velocity_angle = self.rotate_speed * dt
                # self.expens_energy(dt*self._cost_energy*0.2)
        else:
            self.velocity_angle = 0

        self.rotation += self.velocity_angle

        angle_radians = -math.radians(self.rotation)

        if self.energy > 0:
            if self.key_handler[key.UP]:
                force_x = math.cos(angle_radians) * self.thrust * dt
                force_y = math.sin(angle_radians) * self.thrust * dt
                self.velocity_x += force_x
                self.velocity_y += force_y
                self.expens_energy(dt*self._cost_energy)
                self._time_reload_engine = self._const_reload_engine_time


        self.velocity_x -= self.velocity_x * self.resistance
        self.velocity_y -= self.velocity_y * self.resistance

        self.dx = self.velocity_x * dt
        self.dy = self.velocity_y * dt
        self.da = self.velocity_angle


        if self._time_reload_engine < 0:
            if self.energy < self.max_energy:
                self.energy += dt * self._reload_energy
        else:
            self._time_reload_engine -= dt

        if self._time_reload_weapon < 0:
            self.reload(dt)
        else:
            self._time_reload_weapon -= dt

    def reload(self, dt):
        if self.charge < self.magazine:
            self.charge += dt * self._reload_power

    def is_live(self):
        return self.live > 0
