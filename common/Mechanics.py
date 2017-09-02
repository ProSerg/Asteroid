import math
from pyglet.window import key
from Asteroid.common.ResourceManager import *

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
    def __init__(self, name, type_asteroid, property_manager):
        self._root = name
        self._propertyManager = property_manager
        super(AsteroidMechanics, self).__init__(
            resistance=self._propertyManager.get_parameter(self._root, ObjectParameter.RESISTANCE),
            rotate_speed=self._propertyManager.get_parameter(self._root, ObjectParameter.ROTATE_SPEED),
            thrust=self._propertyManager.get_parameter(self._root, ObjectParameter.THRUST),
        )
        self.live = self._propertyManager.get_parameter(self._root, ObjectParameter.LIVE)
        self.damage = self._propertyManager.get_parameter(self._root, ObjectParameter.DAMAGE)
        self.typeAsteroid = type_asteroid
        self.countSplinters = self._propertyManager.get_parameter(self._root, ObjectParameter.COUNT_SPLINTERS)
        self._get_damage = 0

    def add_damage(self, value):
        self._get_damage += value

    def process_live(self, dt):
        self.live -= self._get_damage
        self._get_damage = 0

    def update(self, dt):
        angle_radians = -math.radians(self.rotation)
        self.velocity_x = math.cos(angle_radians) * self.thrust
        self.velocity_y = math.sin(angle_radians) * self.thrust
        self.dx = self.velocity_x * dt
        self.dy = self.velocity_y * dt
        self.da = self.rotate_speed * dt

    def is_live(self):
        return self.live > 0

class BulletMechanics(BaseMechanics):
    def __init__(self, property_manager, weapon):
        self._root = weapon
        self._propertyManager = property_manager
        super(BulletMechanics, self).__init__(
            resistance=self._propertyManager.get_parameter(self._root, ObjectParameter.RESISTANCE),
            thrust=self._propertyManager.get_parameter(self._root, ObjectParameter.THRUST),
            rotate_speed=self._propertyManager.get_parameter(self._root, ObjectParameter.ROTATE_SPEED),
        )
        self.boom = False
        self.energy = self._propertyManager.get_parameter(self._root, ObjectParameter.ENERGY)
        self.damage = self._propertyManager.get_parameter(self._root, ObjectParameter.DAMAGE)
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
    def __init__(self, bonus, live):
        super(StarMechanics, self).__init__(
            resistance=0,
            rotate_speed=0,
            thrust=0,
        )
        self.bonus = bonus
        self.live = live
        self.used = False

    def destroy(self):
        self.live = -1

    def process_live(self, dt):
        self.live -= dt

    def is_live(self):
        return self.live > 0

class FighterMechanics(BaseMechanics):

    def __init__(self, property_manager):
        self._propertyManager = property_manager
        self._root = "fighter"
        super(FighterMechanics, self).__init__(
            resistance=self._propertyManager.get_parameter(self._root, ObjectParameter.RESISTANCE),
            thrust=self._propertyManager.get_parameter(self._root, ObjectParameter.THRUST),
            rotate_speed=self._propertyManager.get_parameter(self._root, ObjectParameter.ROTATE_SPEED),
        )

        self.live = self._propertyManager.get_parameter(
            self._root, ObjectParameter.LIVE)

        self.power_bank = self._propertyManager.get_parameter(
            self._root, ObjectParameter.POWER_BANK)

        self.weapon = self._propertyManager.get_parameter(
            self._root, ObjectParameter.WEAPON)

        # weapon
        self.magazine = self._propertyManager.get_parameter(
            self.weapon, ObjectParameter.MAGAZINE)

        self._cost_bullet = self._propertyManager.get_parameter(
            self.weapon, ObjectParameter.COST_BULLET)

        self._reload_magazine = self._propertyManager.get_parameter(
            self.weapon, ObjectParameter.RECOVERY_MAGAZINE)

        self._const_reload_weapon_time = self._propertyManager.get_parameter(
            self.weapon, ObjectParameter.CONST_RELOAD_WEAPON_TIME)

        # engine
        self._reload_energy = self._propertyManager.get_parameter(
            self._root, ObjectParameter.RECOVERY_ENERGY)

        self._consumption_energy = self._propertyManager.get_parameter(
            self._root, ObjectParameter.CONSUMPTION_ENERGY)

        self._reset_engine = self._propertyManager.get_parameter(
            self._root, ObjectParameter.RESET_ENGINE)

        self._const_recovery_engine_time = self._propertyManager.get_parameter(
            self._root, ObjectParameter.CONST_RECOVERY_ENGINE_TIME)

        self._const_reset_engine_time = self._propertyManager.get_parameter(
            self._root, ObjectParameter.CONST_RESET_ENGINE_TIME)

        self._const_rotate_factor = self._propertyManager.get_parameter(
            self._root, ObjectParameter.CONST_ROTATE_FACTOR)

        self._const_rotate_step_factor = self._propertyManager.get_parameter(
            self._root, ObjectParameter.CONST_ROTATE_STEP_FACTOR)

        self._rotate_factor = self._const_rotate_factor

        self.charge = self.magazine
        self.starting_live = self.live
        self.energy = self.power_bank

        self.key_handler = key.KeyStateHandler()
        self._time_reload_weapon = 0
        self._time_reload_engine = 0
        self._get_damage = 0
        self._moving = False
        self._bool_reset = False

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
        energy = (self.energy / float(self.power_bank))
        if energy > 1.0:
            energy = 1.0
        return energy

    def reset(self):
        self.live = self.starting_live
        self.charge = self.magazine
        self.energy = self.power_bank
        self._get_damage = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_angle = 0

    def add_damage(self, value):
        self._get_damage += value

    def expens_energy(self, value):
        self.energy -= value

    def shoot(self):
        if self.charge > self._cost_bullet:
            self.charge -= self._cost_bullet
            self._time_reload_weapon = self._const_reload_weapon_time
            return True
        return False

    def process_live(self, dt):
        self.live -= self._get_damage
        self._get_damage = 0

    def update(self, dt):
        force_x = 0
        force_y = 0
        if self.key_handler[key.LEFT]:
            if self.energy <= 0:
                self.velocity_angle = -self.rotate_speed * dt * self._rotate_factor * 0.5
            else:
                self.velocity_angle = -self.rotate_speed * dt * self._rotate_factor
            if self._rotate_factor < 1.0:
                self._rotate_factor += self._const_rotate_step_factor

        elif self.key_handler[key.RIGHT]:
            if self.energy <= 0:
                self.velocity_angle = self.rotate_speed * dt * self._rotate_factor * 0.5
            else:
                self.velocity_angle = self.rotate_speed * dt * self._rotate_factor
            if self._rotate_factor < 1.0:
                self._rotate_factor += self._const_rotate_step_factor
        else:
            self.velocity_angle = 0
            self._rotate_factor = self._const_rotate_factor

        self.rotation += self.velocity_angle

        angle_radians = -math.radians(self.rotation)

        if self.energy > 0:
            if self.key_handler[key.UP]:
                force_x = math.cos(angle_radians) * self.thrust * dt
                force_y = math.sin(angle_radians) * self.thrust * dt
                self.velocity_x += force_x
                self.velocity_y += force_y
                self.expens_energy(dt*self._consumption_energy)
                self._time_reload_engine = self._const_recovery_engine_time
        else:
            if self._bool_reset is False:
                self._time_reload_engine = self._const_reset_engine_time
                self._bool_reset = True

        self.velocity_x -= self.velocity_x * self.resistance
        self.velocity_y -= self.velocity_y * self.resistance

        self.dx = self.velocity_x * dt
        self.dy = self.velocity_y * dt
        self.da = self.velocity_angle

        if self._time_reload_engine < 0:
            if self._bool_reset is True:
                self.energy += self.power_bank * self._reset_engine
                self._bool_reset = False
            if self.energy < self.power_bank:
                self.energy += dt * self._reload_energy
        else:
            self._time_reload_engine -= dt

        if self._time_reload_weapon < 0:
            self.reload(dt)
        else:
            self._time_reload_weapon -= dt

    def reload(self, dt):
        if self.charge < self.magazine:
            self.charge += dt * self._reload_magazine

    def is_live(self):
        return self.live > 0
