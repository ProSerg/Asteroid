import Asteroid.common.Resources as Resources
from Asteroid.Items.ItemObject import ItemObject
import pyglet

class UserUI(object):

    def __init__(self, unit_manager, group, batch, *args, **kwargs):
        self._batch = batch

        self.ship = unit_manager.get_sprite(
            name="player_ship.png",
            scale=0.05,
            rotation=0,
            group=group,
        )

        self._score = pyglet.text.Label(
            text='Score: 0',
            x=50, y=575,
            anchor_x='center',
            batch=self._batch)

        self._ammo = pyglet.text.Label(
            text='Ammo: 100 %',
            x=20, y=30,
            anchor_x='left',
            batch=self._batch)

        self._energy = pyglet.text.Label(
            text='Energy: 100 %',
            x=600, y=30,
            anchor_x='left',
            batch=self._batch)

        self._live = pyglet.text.Label(
            text='x 0',
            x=750, y=570,
            anchor_x='left',
            batch=self._batch)

        self.ship.x = 730
        self.ship.y = 578

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
            batch=self._batch))

    def textProgress(selp, procent,  prefix='', suffix='', decimals=1, length=15, fill='='):
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

    def update_live(self, value):
         self._live.text = 'x {}'.format(value)

    def update_energy(self, value):
        self._energy.text = self.textProgress(procent=value)

