import pyglet

from Asteroid.common.ResourceManager import *


class UserUI(object):

    def __init__(self, unit_manager, property_manager, group, batch, *args, **kwargs):
        self._batch = batch
        self._unit_manager = unit_manager
        self._propertyManager = property_manager
        self._group = group

        self.ship = None

        self._score = pyglet.text.Label(
            text='Score: 0',
            x=50, y=575,
            anchor_x='center',
            batch=self._batch,
            group=group)

        self._ammo = pyglet.text.Label(
            text='Ammo: 0 %',
            x=20, y=30,
            anchor_x='left',
            batch=self._batch,
            group=group)

        self._energy = pyglet.text.Label(
            text=self.textProgress(),
            x=600, y=30,
            anchor_x='left',
            batch=self._batch,
            group=group)

        self._live = pyglet.text.Label(
            text='x 0',
            x=750, y=570,
            anchor_x='left',
            batch=self._batch,
            group=group)

        self._gameover = pyglet.text.Label(
            text='',
            x=370, y=370,
            anchor_x='left',
            batch=self._batch,
            group=group)

        self._status = pyglet.text.Label(
            text='',
            x=350, y=330,
            anchor_x='left',
            batch=self._batch,
            group=group)


        # self._armor = pyglet.text.Label(
        #     text='Armor: 100 %',
        #     x=600, y=575,
        #     anchor_x='left',
        #     batch=self._batch)

        self._elements = []
        self._elements.append(self._score)
        self._elements.append(self._ammo)
        self._elements.append(self._energy)
        # self._elements.append(self._armor)

        self._elements.append(pyglet.text.Label(
            text="Asteroids",
            x=400, y=575,
            anchor_x='center',
            batch=self._batch,
            group=group))

    def setShip(self, ship):
        if self.ship:
            self.ship.delete()

        self.ship = self._unit_manager.get_sprite(
            name=self._propertyManager.get_sprite(ship, SpriteParameter.FILENAME),
            scale=0.05,
            rotation=0,
            batch=self._batch,
            group=self._group,
        )

        self.ship.x = 730
        self.ship.y = 578

    def textProgress(selp, procent=1.0,  prefix='', suffix='', decimals=1, length=15, fill='='):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * procent)
        filledLength = int(length*procent)
        bar = fill * filledLength + '  ' * (length - filledLength)
        # print(
        text = '%s |%s|' % (prefix, bar)
        # Print New Line on Complete
        return text

    def update_score(self, value):
        self._score.text = 'Score: {}'.format(value)

    def update_ammo(self, value):
        self._ammo.text = ' Ammo:  {} %'.format(value)

    def game_over(self, value, score):
        if value is True:
            self._status.text = "YOUR SCORE : {}".format(score)
            self._gameover.text = "GAME OVER"
        else:
            self._status.text = ""
            self._gameover.text = ""


    def update_live(self, value):
        self._live.text = 'x {}'.format(value)

    def update_energy(self, value):
        self._energy.text = self.textProgress(procent=value)

