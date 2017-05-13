import pyglet
from pyglet.image import Animation, AnimationFrame
from pyglet.resource import Loader

from Asteroid.common.Sprite import ASprite


class Fabric(object):

    def __init__(self, loader, batch):
        self.loader = loader
        self.batch = batch

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

    def get_animation_effect(self,
                             image_names=[],
                             x=0, y=0, rotation=0, duration=1.0, group=None, scale=1.0,
                             anchor_x=0, anchor_y=0 , anchor="center" ):

        animation = self.loader.create_animation(
            image_names,
            duration=duration,
            loop=False,
            rotate=rotation,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
        )

        new_sprite = ASprite(
            img=animation,
            group=group,
            batch=self.batch,
            x=x,
            y=y,
            rotation=rotation,
            scale=scale,
        )
        return new_sprite


    def get_animation(self, image_names=[], x=0, y=0, rotation=0, duration=1.0, group=None, scale=1.0, anchor_x=0, anchor_y=0 , anchor="center" ):
        animation = self.loader.create_animation(
            image_names,
            duration=duration,
            loop=True,
            rotate=rotation,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
        )

        new_sprite = ASprite(
            img=animation,
            group=group,
            batch=self.batch,
            x=x,
            y=y,
            rotation=rotation,
            scale=scale,
        )
        return new_sprite


class ResourcesLoader(Loader):
    path_to_resource = "../resources"
    resource_paths = [
        "".join((path_to_resource, "/Blue")),
        "".join((path_to_resource, "/Effects/Blue Effects")),
        "".join((path_to_resource, "/Effects/Galaxy")),
        "".join((path_to_resource, "/Effects/Grids")),
        "".join((path_to_resource, "/Effects/Proton Star")),
        "".join((path_to_resource, "/Effects/Red Explosion")),
        "".join((path_to_resource, "/Effects/Fires")),
    ]

    def __init__(self):
        super(ResourcesLoader, self).__init__(path=self.resource_paths)
        self.reindex()

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

    def create_animation(self, image_frames, duration=1.0, loop=False, rotate=0, anchor_x=0, anchor_y=0):
        frames = []
        for img in image_frames:
            image = self.image(img, rotate)
            # self._anchor_image(image, anchor_x, anchor_y)
            self._center_image(image)
            frames.append(AnimationFrame(image, duration))

        if loop is False:
            frames[len(image_frames) - 1].duration = None
        return Animation(frames=frames)

    def create_animation_by_rows(self, image_name, duration, brow, rows, column, columns):
        effect_seq = pyglet.image.ImageGrid(self.image(image_name), rows, columns)
        effect_frames = []
        end = brow * columns
        start = end - (columns - 1)
        for effect_frame in effect_seq[start:end:1]:
            effect_frames.append(AnimationFrame(effect_frame, duration))

        effect_frames[((rows-brow) * (columns -column) ) -1].duration = None
        return Animation(effect_frames)

    def create_animation_by_grids(self, image_name, duration, rows, columns):
        effect_seq = pyglet.image.ImageGrid(self.image(image_name), rows, columns)
        effect_frames = []
        for row in range(rows, 0, -1):
            end = row * columns
            start = end - (columns - 1) - 1
            for effect_frame in effect_seq[start:end:1]:
                effect_frames.append(AnimationFrame(effect_frame, duration))
        effect_frames[(rows * columns) - 1].duration = None
        return Animation(effect_frames)
