import os

import pyglet
from pyglet.image import Animation, AnimationFrame
from pyglet.resource import Loader

from .ResourceManager import *


class ResourcesLoader(Loader):
    background = pyglet.graphics.OrderedGroup(0)
    foreground = pyglet.graphics.OrderedGroup(1)
    ship_group = pyglet.graphics.OrderedGroup(2)
    asteroids_group = pyglet.graphics.OrderedGroup(3)
    effects = pyglet.graphics.OrderedGroup(4)
    ui = pyglet.graphics.OrderedGroup(5)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    path_to_resource = "%s\\..\\..\\resources\\" % dir_path
    resource_paths = [
        os.path.realpath("".join((path_to_resource, "/"))),
        os.path.realpath("".join((path_to_resource, "/Audio"))),
        os.path.realpath("".join((path_to_resource, "/Audio/Asteroid"))),
        os.path.realpath("".join((path_to_resource, "/Audio/Bonus"))),
        os.path.realpath("".join((path_to_resource, "/Audio/Bullet"))),
        os.path.realpath("".join((path_to_resource, "/Audio/Engine"))),
        os.path.realpath("".join((path_to_resource, "/Audio/Envirement"))),
        os.path.realpath("".join((path_to_resource, "/Audio/Game"))),
        os.path.realpath("".join((path_to_resource, "/Audio/Portal"))),
        os.path.realpath("".join((path_to_resource, "/Audio/Ship"))),
        os.path.realpath("".join((path_to_resource, "/Blue"))),
        os.path.realpath("".join((path_to_resource, "/Effects/Blue Effects"))),
        os.path.realpath("".join((path_to_resource, "/Effects/Galaxy"))),
        os.path.realpath("".join((path_to_resource, "/Effects/Grids"))),
        os.path.realpath("".join((path_to_resource, "/Effects/Proton Star"))),
        os.path.realpath("".join((path_to_resource, "/Effects/Red Explosion"))),
        os.path.realpath("".join((path_to_resource, "/Effects/Fires"))),
        os.path.realpath("".join((path_to_resource, "/Asteroids"))),
        os.path.realpath("".join((path_to_resource, "/Background"))),
    ]

    properties = {
        "fighter": "fighterProperty.json",
        "bug": "bugProperty.json",
        "saucer": "saucerProperty.json",
        "smallAsteroid": "smallAsteroidProperty.json",
        "mediumAsteroid": "mediumAsteroidProperty.json",
        "bigAsteroid": "bigAsteroidProperty.json",
        "aBullet": "aBullet.json",
        "sBullet": "sBullet.json",
        "wBullet": "wBullet.json",
        "smallStar": "smallStarProperty.json",
        "mediumStar": "mediumStarProperty.json",
        "bigStar": "bigStarProperty.json",
    }

    sounds = {
        "bum" : "scrape.mp3",
        "destroy" : "space_dead.mp3",
        "portal" : "portal.mp3",
        "shot" : "shot.mp3",
    }

    spring = {}

    def __init__(self):
        self.resource_paths = self.resource_paths
        super(ResourcesLoader, self).__init__(path=self.resource_paths)
        self.reindex()

        for key, value in self.sounds.items():
            # p_spring = pyglet.media.load(
            # "{path}\\{file}".format(
            #     path=os.path.realpath("%s\\Audio\\" % self.path_to_resource),
            #     file=value)
            p_spring = self.media(value, streaming=False)
            self.spring.update({key: p_spring})
        # TODO

        self.jsonManager = JsonManager( work_dir=os.path.realpath("%s\\..\\resources\\" % self.dir_path))
        for key, value in self.properties.items():
            self.jsonManager.addJsonData(key, value)

    def getSpring(self, id_spring):
        print(self.spring)
        return self.spring[id_spring]

    def getPropertyManager(self):
        return PropertyManager(self.jsonManager)


    def _center_image(self, image):
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2

    def create_image(self, image, rotate=0, anchor="", *args):
        img = self.image(image, rotate=rotate)
        if anchor == "center":
            self._center_image(img)
        return img

    def _anchor_image(self, image, anchor_x, anchor_y):
        """Sets an image's anchor point to its center"""
        image.anchor_x = anchor_x
        image.anchor_y = anchor_y

    def create_animation_by_frames(self, image_frames, duration=1.0, rotation=0, looped=False, anchor_x=0, anchor_y=0):
        frames = []
        for img in image_frames:
            image = self.image(img, rotation)
            self._anchor_image(image, anchor_x, anchor_y)
            # self._center_image(image)
            frames.append(AnimationFrame(image, duration))

        if looped is False:
            frames[len(image_frames) - 1].duration = None
        return Animation(frames=frames)

    def create_animation_by_gif(self, image_name):
        image = self.animation(name=image_name)
        return image

    def create_animation_by_rows(self, image_name, duration, rotation, brow, rows, column, columns):
        effect_seq = pyglet.image.ImageGrid(self.image(image_name, rotation), rows, columns)
        effect_frames = []
        end = brow * columns
        start = end - (columns - 1)
        for effect_frame in effect_seq[start:end:1]:
            effect_frames.append(AnimationFrame(effect_frame, duration))

        effect_frames[((rows-brow) * (columns - column) ) -1].duration = None
        return Animation(effect_frames)

    def create_animation_by_grids(self, image_name, duration, rotation, rows, columns):
        effect_seq = pyglet.image.ImageGrid(self.image(image_name, rotation), rows, columns)
        effect_frames = []
        for row in range(rows, 0, -1):
            end = row * columns
            start = end - (columns - 1) - 1
            for effect_frame in effect_seq[start:end:1]:
                effect_frames.append(AnimationFrame(effect_frame, duration))
        effect_frames[(rows * columns) - 1].duration = None
        return Animation(effect_frames)

    def create_animation_by_grids_inverse(self, image_name, duration, rotation, rows, columns):
        effect_seq = pyglet.image.ImageGrid(self.image(image_name, rotation), rows, columns)
        effect_frames = []
        for row in range(rows, 0, -1):
            end = row * columns
            start = end - (columns - 1) - 1
            for effect_frame in effect_seq[start:end:1]:
                effect_frames.append(AnimationFrame(effect_frame, duration))
        effect_frames[(rows * columns) - 1].duration = None
        return Animation(effect_frames)