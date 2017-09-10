import pyglet, copy
from pyglet.image import Animation, AnimationFrame
from pyglet.resource import Loader

import queue


class AnimationSprite(pyglet.sprite.Sprite):
    def __init__(self, img , looped, calldelete, scale, rotation, *args, **kwargs):
        super(AnimationSprite, self).__init__(img=img, *args, **kwargs)
        self.image_buffer = self.image
        self._animation_ended = False
        self._looped = looped
        self._calldelete = calldelete
        self.rotation = rotation
        self.scale = scale

    def restart(self):
        if self._animation_ended is True:
            self.image = self.image_buffer
            self._animation_ended = False

    def on_animation_end(self):
        if self._looped is True:
            self._animation_ended = True
        else:
            if self._calldelete:
                self._calldelete(self)
            self.delete()

    def move(self, dx=0, dy=0, da=0.0 ):
        """
        переместить объект на значения.
        :param dx:
        :param dy:
        :param da:
        :return:
        """
        self.x += dx
        self.y += dy

    def turn(self, theata, dt):
        pass

    def destoy(self):
        pass


class AnimationManager(object):
    def __init__(self, loader):
        self.loader = loader
        self._buffer_springs_effects = {}
        self._animations = []

    def getSpringEffect(self, img, type_image, batch, group, rotation, scale, **kwargs):
        if type_image == "grid":
            frames = self.loader.create_animation_by_grids(img,
                duration=kwargs["duration"],
                rows=kwargs["rows"],
                columns=kwargs["columns"])
        elif type_image == "frames":
            frames = self.loader.create_animation_by_frames(img,
                duration=kwargs["duration"],
                looped=kwargs["looped"])
        elif type_image == "gif":
            frames = self.loader.create_animation_by_gif(img)
        else:
            frames = None
        if frames:
            return AnimationSprite(frames,
                    looped=kwargs["looped"],
                    scale=scale,
                    rotation=rotation,
                    calldelete=None,
                    batch=batch,
                    group=group)
        else:
            return None

    def createSpringEffect(self, name, img, scale, type_image, inverse=False, **kwargs ):
        if type_image == "grid":
            if inverse is True:
                frames = self.loader.create_animation_by_grids_inverse(img,
                    duration=kwargs["duration"],
                    rows=kwargs["rows"],
                    columns=kwargs["columns"],
                    rotation=kwargs["rotation"])
            else:
                frames = self.loader.create_animation_by_grids(img,
                    duration=kwargs["duration"],
                    rows=kwargs["rows"],
                    columns=kwargs["columns"],
                    rotation=kwargs["rotation"])
        elif type_image == "frames":
            frames = self.loader.create_animation_by_frames(img,
                duration=kwargs["duration"],
                looped=kwargs["looped"],
                rotation=kwargs["rotation"],
                anchor_x=kwargs["rotation"],
                anchor_y=kwargs["rotation"])
        elif type_image == "gif":
            frames = self.loader.create_animation_by_gif(img)
        else:
            frames = None
        if frames:
            self._buffer_springs_effects.update(
                { name: {
                    "frames": frames,
                    "scale": scale,
                    }
                }
            )
            return 0
        else:
            return -1

    def deleteAnimation(self, obj):
        self._animations.remove(obj)
        pass

    def Play(self):
        for item in self._animations:
            item.draw()

    def playAnimation(self, name,  x=0, y=0, rotation=0, looped=False, batch=None, group=None):
        animation = AnimationSprite(self._buffer_springs_effects.get(name).get("frames"),
                                    scale=self._buffer_springs_effects.get(name).get("scale"),
                                    looped=looped, calldelete=self.deleteAnimation, rotation=rotation,
                                    batch=batch, group=group)
        # animation.set_position(x - animation.width/2, y -  animation.height/2)
        # animation.set_position(x - animation.width/2, y - animation.height/2)
        animation.set_position(x - animation.width/2, y - animation.height/2)
        self._animations.append(animation)

    def createAnimation(self, name,  x=0, y=0, rotation=0, looped=False, batch=None, group=None):
        animation = AnimationSprite(self._buffer_springs_effects.get(name).get("frames"),
                                    scale=self._buffer_springs_effects.get(name).get("scale"),
                                    looped=looped, calldelete=None, rotation=rotation,
                                    batch=batch, group=group)
        # animation.set_position(x - animation.width/2, y - animation.height/2)
        animation.set_position(x - animation.width/2, y - animation.height/2)
        return animation

    def getAnimation(self, name,  x=0, y=0):
        animation = self._buffer_springs_effects.get(name)
        animation.set_position(x - animation.width/2, y - animation.height/2)
        return animation

"""
w : switch background to white
b : switch background to black
1 - 5 : change particle effect
Left Mouse click : spawn new effect at mouse location
"""