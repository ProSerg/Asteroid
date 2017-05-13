import Asteroid.common.Resources as Resources
from Asteroid.Items.ItemObject import ItemObject
import pyglet

class UserUI(object):

    def __init__(self, batch, *args, **kwargs):
        self._batch = batch
        self._elements = []
        self._elements.append(pyglet.text.Label(
            text="Score: 0",
            x=10, y=575,
            batch=self._batch))

        self._elements.append(pyglet.text.Label(
            text="Asteroids",
            x=400, y=575,
            anchor_x='center',
            batch=self._batch))