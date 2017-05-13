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
from Asteroid.GameMaster import GameMaster


class BatchOp(object):
    def __init__(self, name, status=True):
        self.batch = pyglet.graphics.Batch()
        self.name = name
        self.status = status


class GameScene(pyglet.window.Window):
    __BATCH_MAIN_NAME__ = "main_batch"

    def __init__(self, width, height, DEBUG_MOD=False):
        super(GameScene, self).__init__(width, height)
        # self.window = pyglet.window.Window(width, height)
        self.pages = []
        self.labels = []
        self.interface = []
        self.items = []
        self.batches = {}
        self.sprites = []
        self._curr_batch = None
        # self.main_batch = BatchOp(self.__BATCH_MAIN_NAME__)
        self.create_batch(self.__BATCH_MAIN_NAME__)
        self.set_main_batch(self.__BATCH_MAIN_NAME__)
        self._dt = 1 / 120.0
        pyglet.clock.schedule_interval(self.update, self._dt)
        # self.key_handler = key.KeyStateHandler()
        self.fps_display = pyglet.window.FPSDisplay(window=self)

        self._debug = DEBUG_MOD
        self.master = GameMaster(batch=self.get_batch())
        self.user_ship = None


    def checkForCollision(self, obj1, obj2):
        # if (obj1.x < obj2.x + obj2.width) \
        #         and (obj2.x < obj1.x + obj1.width) \
        #         and (obj1.y < obj2.y + obj2.height) \
        #         and (obj2.y < obj1.y + obj1.height)
        #     return True
        # return False
        pass

    def generate_scene(self):
        import random
        self.user_ship = self.master.make_user_ship(x=300, y=400, rotation=-45, rotate_speed=180, thrust=310)
        self.push_handlers(self.user_ship.mechanic.key_handler)
        self.add_item(self.user_ship)

        for num in range(10):
            asteroid = self.master.make_asteroid(
                x=random.randint(0, 500),
                y=random.randint(0, 400),
                rotation=random.randint(0, 180),
                rotate_speed=random.randint(-200, 200),
                thrust=random.randint(100, 600))
            self.add_item(asteroid)


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

    def add_item(self, item):
        self.items.append(item)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.W:
            self.shoot = True
            if self.user_ship.live:
                bullet = self.master.make_bullet(
                    x=self.user_ship.x,
                    y=self.user_ship.y,
                    rotation=self.user_ship.rotation)
                self.add_item(bullet)

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.W:
            self.shoot = False

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
        if type(obj1) is PlayerShip or type(obj2) is PlayerShip:
            distance = util.distance(obj1.get_center(), obj2.get_center())
            if (distance <= (obj1.figure.radius + obj2.figure.radius)) is True:
                obj1.add_collision_obj(obj2)
                obj2.add_collision_obj(obj1)

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


    def processing_collisions(self):
        objects = self._get_objects()
        for obj in objects:
            if obj.static is False:
                self.check_bounds(obj)

        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                self.check_collision(objects[i], objects[j])

    def processing_objects(self):
        objects = self._get_objects()
        for obj in objects:
            obj.process()
            if obj.live is False:
                obj.destroy()
                objects.remove(obj)
                del obj
                obj = None


    def update(self, _dt):
        self.processing_collisions()
        self.moving(_dt)
        self.processing_objects()

if __name__ == "__main__":
    game = GameScene(800, 600)
    # game.add_label(text="Score: 0", x=10, y=575)
    # pyglet.app.run()