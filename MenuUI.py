import Asteroid.common.Resources as Resources
from Asteroid.Items.ItemObject import ItemObject
import pyglet
from Asteroid.common.ResourceManager import *
from GameMaster import TypeShip

class MenuUI(object):

    def __init__(self, unit_manager, property_manager,  group, batch, *args, **kwargs):
        self._batch = batch
        self._propertyManager = property_manager

        self.ship = unit_manager.get_sprite(
            name=self._propertyManager.get_sprite(TypeShip.FIGHTER.value, SpriteParameter.FILENAME),
            scale=0.05,
            rotation=0,
            batch=self._batch,
            group=group,
        )

        self.ship.x = 350
        self.ship.y = 400

        self.bug = unit_manager.get_sprite(
            name=self._propertyManager.get_sprite(TypeShip.BUG.value, SpriteParameter.FILENAME),
            scale=0.05,
            rotation=0,
            batch=self._batch,
            group=group,
        )

        self.bug.x = 350
        self.bug.y = 350

        self.saucer = unit_manager.get_sprite(
            name=self._propertyManager.get_sprite(TypeShip.SAUCER.value, SpriteParameter.FILENAME),
            scale=0.05,
            rotation=0,
            batch=self._batch,
            group=group,
        )

        self.saucer.x = 350
        self.saucer.y = 300

        self._label_fighter = pyglet.text.Label(
            text='1.           Fighter',
            x=310, y=395,
            anchor_x='left',
            batch=self._batch,
            group=group)

        self._label_bug = pyglet.text.Label(
            text='2.           Bug',
            x=310, y=345,
            anchor_x='left',
            batch=self._batch,
            group=group)

        self._label_saucer = pyglet.text.Label(
            text='3.           Saucer',
            x=310, y=295,
            anchor_x='left',
            batch=self._batch,
            group=group)

        self._label_exit = pyglet.text.Label(
            text='for Exit press \'ESCAPE\'',
            x=310, y=50,
            anchor_x='left',
            batch=self._batch,
            group=group)

        self._label_start = pyglet.text.Label(
            text='for Start press \'ENTER\' (return menu F10)',
            x=310, y=450,
            anchor_x='left',
            batch=self._batch,
            group=group)

        self.color_white = (255, 255, 255, 255)
        self.color_red = (255, 0, 0, 255)


    def select_choose(self, choose):
        if choose.value == TypeShip.FIGHTER.value:
            self._label_bug.color = self.color_white
            self._label_saucer.color = self.color_white
            self._label_fighter.color = self.color_red
        elif choose.value == TypeShip.BUG.value:
            self._label_bug.color = self.color_red
            self._label_saucer.color = self.color_white
            self._label_fighter.color = self.color_white
        elif choose.value == TypeShip.SAUCER.value:
            self._label_bug.color = self.color_white
            self._label_saucer.color = self.color_red
            self._label_fighter.color = self.color_white




