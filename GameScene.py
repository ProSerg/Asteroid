import pyglet
from pyglet.graphics import *
import Asteroid.common.util as util
from Asteroid.common.Figure import *
from Asteroid.Items.PlayerShip import PlayerShip
import pyglet.gl as gl
from pyglet.window import key
from pathlib import Path
# Set up a window

from Asteroid.common.Resources import *
from Asteroid.common.Figure import *
from Asteroid.common.Mechanics import *
from Asteroid.GameMaster import *
import random

from GameMaster import TypeAsteroid


class BatchOp(object):
    def __init__(self, name, status=True):
        self.batch = pyglet.graphics.Batch()
        self.name = name
        self.status = status


class GameScene(pyglet.window.Window):
    __BATCH_MAIN_NAME__ = "main_batch"
    path_to_resource = "../resources/"
    resource_paths = [
        "".join((path_to_resource, "/Blue")),
        "".join((path_to_resource, "/Effects/Blue Effects")),
        "".join((path_to_resource, "/Effects/Galaxy")),
        "".join((path_to_resource, "/Effects/Grids")),
        "".join((path_to_resource, "/Effects/Proton Star")),
        "".join((path_to_resource, "/Effects/Red Explosion")),
        "".join((path_to_resource, "/Effects/Fires")),
        "".join((path_to_resource, "/Asteroids")),
    ]

    def __init__(self, width, height, DEBUG_MOD=False):
        super(GameScene, self).__init__(width, height)
        # self.window = pyglet.window.Window(width, height)
        self.pages = []
        self.labels = []
        self.interface = []
        self.items = set()
        self.bullets = []
        self.batches = {}
        self.sprites = []
        self._curr_batch = None

        self.create_batch(self.__BATCH_MAIN_NAME__)
        self.set_main_batch(self.__BATCH_MAIN_NAME__)
        self._dt = 1 / 120.0
        pyglet.clock.schedule_interval(self.update, self._dt)
        # self.key_handler = key.KeyStateHandler()
        self.fps_display = pyglet.window.FPSDisplay(window=self)

        self._debug = DEBUG_MOD
        self.loader = ResourcesLoader(self.resource_paths)
        self.master = GameMaster(loader=self.loader , batch=self.get_batch())
        self.user_ship = None
        self._start_ship_position = Point(400, 350)


        ## USER SETTINGS
        self._score = 0
        self._bonus = 0

    def checkForCollision(self, obj1, obj2):
        # if (obj1.x < obj2.x + obj2.width) \
        #         and (obj2.x < obj1.x + obj1.width) \
        #         and (obj1.y < obj2.y + obj2.height) \
        #         and (obj2.y < obj1.y + obj1.height)
        #     return True
        # return False
        pass

    def generate_scene(self):
        self.user_ship = self.master.make_user_ship(
            x=self._start_ship_position.x, y=self._start_ship_position.y,
            rotation=-45, rotate_speed=220, thrust=400)
        self.push_handlers(self.user_ship.mechanic.key_handler)
        self.user_ship.visible(False)


    def create_batch(self, name, status=True):
        self._curr_batch = BatchOp(name, status)
        self.batches.update({name: self._curr_batch})

    def get_batch(self, name=None):
        if name is not None:
            return self.batches.get(name).batch
        else:
            return self._curr_batch.batch

    def set_main_batch(self, name):
        self.main_batch = self.batches.get(name).batch

    def add_label(self, label):
        self.labels.append(label)

    def get_labels(self):
        return self.labels

    def add_interface(self, item):
        self.interface.append(item)

    def del_item(self, item):
        self.items.remove(item)

    def add_item(self, item):
        self.items.add(item)

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def on_mouse_press(self, x, y, button, modifiers):
        print("press ", x, y)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.W:
            if self.user_ship.getVisible() is True:
                if self.user_ship.mechanic.shoot() is True:
                    bullet = self.master.make_bullet(
                        x=self.user_ship.x,
                        y=self.user_ship.y,
                        rotation=self.user_ship.rotation,
                        energy=500)
                    self.add_bullet(bullet)
        elif symbol == pyglet.window.key.SPACE:
            self.usePortal()
        elif symbol == pyglet.window.key.R:
            self.create_wave()
        elif symbol == pyglet.window.key.ESCAPE:
            self.clear_wave()

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.W:
            pass

    def on_draw(self):
        self.clear()
        for name, batch_op in self.batches.items():
            if batch_op.status is True:
                batch_op.batch.draw()

        if self._debug is True:
            for item in self._get_objects():
                try:
                    item.draw()
                except Exception as ex:
                    continue

            self.fps_display.draw()
            # pyglet.graphics.draw(
            #     2,
            #     pyglet.gl.GL_LINES,
            #     ('v2f', (0, 0, 800, 600)))


    def _get_objects(self):
        return self.items

    def check_collision(self, obj1 , obj2):
    # if type(obj1) is PlayerShip or type(obj2) is PlayerShip:
    #     distance = util.distance(obj1.get_center(), obj2.get_center())
    #     if (distance <= (obj1.figure.radius + obj2.figure.radius)) is True:
    #         obj1.add_collision_obj(obj2)
    #         obj2.add_collision_obj(obj1)

        if obj2 == obj1:
            return False
        else:
            if (obj1.x < obj2.x + obj2.bounds.width) \
                and (obj2.x < obj1.x + obj1.bounds.width) \
                and (obj1.y < obj2.y + obj2.bounds.height) \
                and (obj2.y < obj1.y + obj1.bounds.height):
                return True
            else:
                return False

    def check_hit(self, bullet, asteroid):
        rx = asteroid.x - asteroid.bounds.width / 2
        ry = asteroid.y - asteroid.bounds.height / 2
        width = asteroid.bounds.width
        height = asteroid.bounds.height
        cx = bullet.x
        cy = bullet.y
        radius = bullet.bounds.radius
        return self.isCircleToRect(cx, cy, radius, rx, ry, width, height)

    def isCircleToRect(self, cx, cy, radius, rx, ry, width, height):
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

    def check_bounds(self, item):
        """Use the classic Asteroids screen wrapping behavior"""
        figure = item.bounds
        if figure is not None:
            x = item.x
            y = item.y
            min_x = -figure.width / 2
            min_y = -figure.height / 2
            max_x = self.width + figure.width / 2
            max_y = self.height + figure.height / 2
            flag = False
            if x < min_x:
                 x = max_x
                 flag = True
            elif x > max_x:
                 x = min_x
                 flag = True
            if y < min_y:
                 y = max_y
                 flag = True
            elif y > max_y:
                 y = min_y
                 flag = True
            if flag is True:
                item.update_pos(x, y)


    def moving(self, _dt):
        for obj in self._get_objects():
            if obj.static is False:
                obj.update(_dt)

        for bullet in self.bullets:
            bullet.update(_dt)

    def processing_collisions(self):
        '''
        Обработчик столкновений определяет если были столкновений, то взависимости что с чем столкнулось
        получет повредждения. А также вектор визического удара.
        :return:
        '''
        objects = self._get_objects()
        for obj in objects:
            if obj.static is False:
                self.check_bounds(obj)

        for obj in self.bullets:
            if obj.static is False:
                self.check_bounds(obj)

        # for i in range(len(objects)):
        #     for j in range(i + 1, len(objects)):
        #         self.check_collision(objects[i], objects[j])
        flag = False
        for obj in objects.copy():
            if obj.name.find("Asteroid") != -1:
                if self.check_collision(self.user_ship, obj) is True:
                    # flag = True
                    # self.master.play(
                    #     "ship_boom",
                    #     self.user_ship.sprite.x, self.user_ship.sprite.y)
                    #self.items.pop(self.items.index(self.user_ship))
                    # self.user_ship.visible = False
                    # self.user_ship.live = False
                    print("Damage:!!")
                    self.user_ship.mechanic.add_damage(value=300)
                for bullet in self.bullets:
                    if self.check_hit(bullet, obj) is True:
                        # obj.bounds.color = Color.Red
                        obj.mechanic.add_damage(value=bullet.mechanic.damage)
                        bullet.mechanic.destroy()

        if flag is True:
            self.user_ship.bounds.color = Color.Red
        else:
            self.user_ship.bounds.color = Color.Green


    def processing_objects(self):
        '''
        Обработчик объектов. Проверяет состояние параметров. Например, проверяет если у объекта закончились жизни, то
        уничтожает. Или получил повреждения, то вычитает.
        :return:
        '''
        objects = self._get_objects()
        for obj in objects.copy():
            if obj.name.find("Asteroid") > -1:
                obj.process()
                if obj.live is False:
                    self.master.play(
                        "asteroid_boom",
                        obj.sprite.x, obj.sprite.y, group=self.loader.effects)
                    typeAsteroid = obj.mechanic.typeAsteroid.value
                    if TypeAsteroid.MEDIUM.value == typeAsteroid:
                        for idx in range(0, 3):
                            asteroid = self.master.make_asteroid(
                                name="Asteroid",
                                x=obj.sprite.x,
                                y=obj.sprite.y,
                                rotation=random.randint(0, 360),
                                rotate_speed=obj.mechanic.rotate_speed - int(obj.mechanic.rotate_speed*0.1),
                                thrust=obj.mechanic.thrust - int( obj.mechanic.thrust*0.1),
                                type=TypeAsteroid.SMALL)
                            self.add_item(asteroid)
                            self._bonus = 5
                    elif TypeAsteroid.BIG.value == typeAsteroid:
                        for idx in range(0, 5):
                            asteroid = self.master.make_asteroid(
                                name="Asteroid",
                                x=obj.sprite.x,
                                y=obj.sprite.y,
                                rotation=random.randint(0, 360),
                                rotate_speed=obj.mechanic.rotate_speed - int(obj.mechanic.rotate_speed*0.1),
                                thrust=obj.mechanic.thrust - int(obj.mechanic.thrust*0.1),
                                type=TypeAsteroid.SMALL)
                            self.add_item(asteroid)
                            self._bonus = 10
                    else:
                        self._bonus = 0

                    self.del_item(obj)
                    obj.destroy()
                    del obj
                    obj = None

                    self._score += 1 + self._bonus
            else:
                self.user_ship.process()
                if self.user_ship.live is False:
                    self.user_ship.visible(False)
                    self.master.play(
                        "ship_boom",
                        self.user_ship.sprite.x, self.user_ship.sprite.y, group=self.loader.effects)
                    self.del_item(self.user_ship)

        for obj in self.bullets:
            obj.process()
            if obj.live is False:
                if obj.mechanic.boom is True:
                    self.master.play(
                        "bullet_boom",
                        obj.sprite.x, obj.sprite.y, group=self.loader.effects)
                self.bullets.remove(obj)
                del obj
                obj = None

    def processing_environment(self):
        self.master.user_ui.update_score(self._score)
        self.master.user_ui.update_ammo(self.user_ship.mechanic.getAmmo())
        self.master.user_ui.update_energy(self.user_ship.mechanic.getEnergy())


    def update(self, _dt):
        self.processing_collisions()
        self.moving(_dt)
        self.processing_objects()
        self.processing_environment()


    def clear_wave(self):
        for obj in self._get_objects():
            if obj.name.find("Asteroid") != -1:
                obj.mechanic.live = 0

    def create_wave(self, numbers=10):
        for num in range(numbers):
            asteroid = self.master.make_asteroid(
                name="Asteroid_{}".format(num),
                x=random.randint(50, 800),
                y=random.randint(700, 750),
                rotation=random.randint(0, 360),
                rotate_speed=random.randint(-200, 200),
                thrust=random.randint(50, 300),
                type=random.choice([TypeAsteroid.BIG, TypeAsteroid.MEDIUM, TypeAsteroid.SMALL]))
            self.add_item(asteroid)


    def arrivalShip(self):
        self.master.play(
            "portal", self._start_ship_position.x, self._start_ship_position.y, group=self.loader.background)
        self.user_ship.update_pos(
            x=self._start_ship_position.x,
            y=self._start_ship_position.y,
        )
        self.user_ship.visible(True)
        self.add_item(self.user_ship)

    def leavingShip(self):
        self.master.play(
            "portal", self.user_ship.sprite.x, self.user_ship.sprite.y, group=self.loader.background)
        self.user_ship.visible(False)
        self.del_item(self.user_ship)

    def usePortal(self):
        if self.user_ship.getVisible() is True and self.user_ship.live is True:
            self.leavingShip()
        elif self.user_ship.live is False:
            self.restart()
        else:
            self.arrivalShip()

    def restart(self):
        self.user_ship.reset()
        self.arrivalShip()
        self.add_item(self.user_ship)

if __name__ == "__main__":
    game = GameScene(800, 600)
    # game.add_label(text="Score: 0", x=10, y=575)
    # pyglet.app.run()