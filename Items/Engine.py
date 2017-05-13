from Asteroid.Items.Unit import Unit
import Asteroid.common.Resources as Resources
import pyglet

class Engine(Unit):
    fire_image = "fire_7.png"

    fire_start_images = (
        "fire_16.png",
        "fire_27.png",
        "fire_34.png")

    fire_work_images = (
        # "fire_48.png",
        # "fire_53.png",
        "fire_71.png",
        "fire_85.png",
        # "fire_94.png",
    )

    def __init__(self, visible=False,
                 *args, **kwargs):
        # image = Resources.make_image(name_file=self.fire_image)
        # image.anchor_x = image.width / 2
        # image.anchor_y = image.height * 1.85
        self.animation()
        super(Engine, self).__init__(
            static=False,
            img=self.anims,
            *args, **kwargs)

    def animation(self):
        try:
            images = map(self.make_sprites, self.fire_work_images)
            self.anims = pyglet.image.Animation.from_image_sequence(images, 0.1)
            # self.animSprite = pyglet.sprite.Sprite(animation)
        except Exception as ex:
            print(ex)

    def make_sprites(self, name_file):
        image = Resources.make_image(name_file)
        image.anchor_x = image.width / 2
        image.anchor_y = image.height * 1.85
        return image

    def on_animation_end(self):
        print("")

# on_animation_end()
# The sprite animation reached the final frame.
# The event is triggered only if the sprite has an animation, not an image.
# For looping animations, the event is triggered each time the animation loops.