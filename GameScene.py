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
from Asteroid.common.ResourceManager import *
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
        "".join((path_to_resource, "/Background")),
    ]
    def __init__(self, width, height,  DEBUG_MOD=False):
        super(GameScene, self).__init__(width, height, self.config)
        # self.window = pyglet.window.Window(width, height)
        self.pages = []
        self.labels = []
        self.interface = []
        self.items = set()
        self.bullets = []
        self.stars = []
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

        self.master.make_star(-50,-50, TypeAsteroid.MEDIUM)
        self.master.make_star(-50,-50, TypeAsteroid.BIG)
        self.master.make_star(-50,-50, TypeAsteroid.SMALL)

        ## USER SETTINGS
        self._score = 0
        self._bonus = 0
        self._ships = 4

        self._shooted = False

        self._mouse_x = 0
        self._mouse_y = 0

        # star = self.master.make_star(100,100,None,100,10)
        # self.stars.append(star)

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
            x=self._start_ship_position.x,
            y=self._start_ship_position.y)
        self.push_handlers(self.user_ship.mechanic.key_handler)
        self.user_ship.visible(False)
        self.arrivalShip()
        self._background = self.master.createBackGround()


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
        try:
            self.items.remove(item)
        except KeyError as ex:
            pass

    def add_item(self, item):
        self.items.add(item)

    def add_bullet(self, bullet):
        if type(bullet) is list:
            self.bullets.extend(bullet)
        else:
            self.bullets.append(bullet)

    def on_mouse_press(self, x, y, button, modifiers):
        print("press ", x, y)
        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x , y, button, modifiers):
        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.usePortal()
        elif symbol == pyglet.window.key.R:
            self.usePortal()
            self.create_wave()
        elif symbol == pyglet.window.key.ESCAPE:
            # self.clear_wave()
            self.restartGame()
        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_key_release(symbol, modifiers)

    def restartGame(self):
        self._score = 0
        self._bonus = 0
        self._ships = 4

        self.user_ship.visible(False)
        self.del_item(self.user_ship)

        while self.items:
            item = self.items.pop()
            item.destroy()

        while self.stars:
            bonus = self.stars.pop()
            bonus.destroy()
            del bonus

        self.user_ship.live = False
        self.usePortal()

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

    def check_collision(self, obj1, obj2):
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
            if obj.typeItem == TypeItem.ASTEROID:
                if self.check_collision(self.user_ship, obj) is True:
                    self.user_ship.mechanic.add_damage(value=obj.mechanic.damage)
                for bullet in self.bullets:
                    if self.check_hit(bullet, obj) is True:
                        # obj.bounds.color = Color.Red
                        if obj.mechanic.live > 0:
                            obj.mechanic.add_damage(value=bullet.mechanic.damage)
                            bullet.mechanic.destroy()

        for star in self.stars:
            if self.check_collision(self.user_ship, star) is True:
                self._score += star.mechanic.bonus
                star.mechanic.destroy()
                star.mechanic.used = True

        if flag is True:
            self.user_ship.bounds.color = Color.Red
        else:
            self.user_ship.bounds.color = Color.Green

    def processing_objects(self, dt):
        '''
        Обработчик объектов. Проверяет состояние параметров. Например, проверяет если у объекта закончились жизни, то
        уничтожает. Или получил повреждения, то вычитает.
        :return:
        '''
        objects = self._get_objects()
        for obj in objects.copy():
            if obj.typeItem == TypeItem.ASTEROID:
                obj.process(dt)
                if obj.live is False:
                    self.master.play(
                        "asteroid_boom",
                        obj.sprite.x, obj.sprite.y, group=self.loader.effects)
                    splinters = self.master.generate_splinters(obj)
                    for item in splinters:
                        self.add_item(item)
                    self.stars.append(self.master.make_star(obj.sprite.x, obj.sprite.y, obj.mechanic.typeAsteroid))
                    self.del_item(obj)
                    obj.destroy()
                    del obj
                    obj = None
            else:
                self.user_ship.process(dt)
                if self.user_ship.live is False:
                    self.user_ship.visible(False)
                    self.master.play(
                        "ship_boom",
                        self.user_ship.sprite.x, self.user_ship.sprite.y, group=self.loader.effects)
                    self.del_item(self.user_ship)
                else:
                    bullet = self.user_ship.mechanic.shot(
                        self.user_ship.x,
                        self.user_ship.y)
                    if bullet:
                        self.add_bullet(bullet)

        for obj in self.bullets:
            obj.process(dt)
            if obj.live is False:
                if obj.mechanic.boom is True:
                    self.master.play(
                        "bullet_boom",
                        obj.sprite.x, obj.sprite.y, group=self.loader.effects)
                self.bullets.remove(obj)
                del obj
                obj = None

        for star in self.stars:
            star.process(dt)
            if star.mechanic.is_live() is False:
                if star.mechanic.used is False:
                    self.master.play(
                        "star_boom",
                        star.sprite.x + 25, star.sprite.y + 25, group=self.loader.effects)
                self.stars.remove(star)
                star.destroy()
                del star
                star = None

    def processing_environment(self):
        self.master.user_ui.update_score(self._score)
        self.master.user_ui.update_ammo(self.user_ship.mechanic.getAmmo())
        self.master.user_ui.update_energy(self.user_ship.mechanic.getEnergy())
        self.master.user_ui.update_live(self._ships)


    def update(self, dt):
        self.moving(dt)
        self.processing_collisions()
        self.processing_objects(dt)
        self.processing_environment()


    def clear_wave(self):
        for obj in self._get_objects():
            if obj.typeItem == TypeItem.ASTEROID:
                obj.mechanic.live = 0

    def create_wave(self, numbers=7):
        for num in range(numbers):
            asteroid = self.master.generate_asteroid(
                name="Asteroid_{}".format(num),
                x=random.randint(50, 800),
                y=random.randint(700, 750))
            self.add_item(asteroid)


    def arrivalShip(self):
        self.master.play(
            "portal", self._start_ship_position.x, self._start_ship_position.y, group=self.loader.effects)
        self.user_ship.update_pos(
            x=self._start_ship_position.x,
            y=self._start_ship_position.y,
        )
        self.user_ship.visible(True)
        self.add_item(self.user_ship)
        self._ships -= 1

    def leavingShip(self):
        self.master.play(
            "portal", self.user_ship.sprite.x, self.user_ship.sprite.y, group=self.loader.effects)
        self.user_ship.visible(False)
        self.del_item(self.user_ship)
        self._ships += 1

    def usePortal(self):
        if self._ships > 0:
            if self.user_ship.live is False:
                self.user_ship.reset()
                self.arrivalShip()


if __name__ == "__main__":
    game = GameScene(800, 600)
    # game.add_label(text="Score: 0", x=10, y=575)
    # pyglet.app.run()