import pyglet
from pyglet.image import Animation, AnimationFrame
from pyglet.resource import Loader
from Asteroid.common.Figure import *
from Asteroid.Items.ItemObject import ItemObject


class ASprite(pyglet.sprite.Sprite):
    def __init__(self, scale=1.0, rotation=0, *args, **kwargs):
        super(ASprite, self).__init__(*args, **kwargs)
        self.scale = scale
        self.rotation = rotation
        self.relative_position = Point(0,0)

    def move(self, dx, dy, da):
        self.set_position(self.x + dx, self.y + dy)
        self.rotation += da

    def update(self, dt):
        pass


class UnitManager(object):

    def __init__(self, loader, batch):
        self.loader = loader
        self.batch = batch
        self._units = []

    def get_sprite(self, name="", x=0, y=0, rotation=0, group=None, scale=1.0, anchor="center"):

        image = self.loader.create_image(image=name, anchor=anchor)

        new_sprite = ASprite(
            img=image,
            group=group,
            batch=self.batch,
            x=x,
            y=y,
            rotation=rotation,
            scale=scale,
        )
        return new_sprite

    def get_bounds(self, figure, *args, **kwargs):
        bound = None
        if figure == "Circle" :
            bound = Circle(*args, **kwargs)
        elif figure == "Rectangle":
            bound = Rectangle(*args, **kwargs)
        return bound

    def add_unit(self, name, sprite, mechanic, bounds):
        item = ItemObject(
            x=x,
            y=y,
            name=name,
            sprite=sprite,
            mechanic=mechanic,
            bounds=bounds,
        )
        self._units.append(item)