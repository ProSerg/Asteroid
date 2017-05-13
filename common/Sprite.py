import pyglet

from Asteroid.common.Point import Point


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
