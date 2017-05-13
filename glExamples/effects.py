import pyglet, copy
from pyglet.image import Animation, AnimationFrame
from pyglet.resource import Loader

import queue

window = pyglet.window.Window()

white = (1, 1, 1, 1)
black = (0, 0, 0, 1)
pyglet.gl.glClearColor(*white)

effects = []
use_effect = 1


resources_paths = [
    "../../resources/Fires",
    "../../resources/Effects/Grids",
    "../../resources/Blue/",
    "../../resources/Animations/gif/",
]

loader = Loader()
loader.path = resources_paths
loader.reindex()


def create_effect(image_frames, duration=1.0, loop=False):
    frames = []
    for img in image_frames:
        image = loader.image(img)
        frames.append(AnimationFrame(image, duration))
    if loop is False:
        frames[len(image_frames) - 1].duration = None
    return Animation(frames=frames)

    # Create a sprite instance.

def create_effect_animation_by_gif(image_name, duration=1.0):
    image = loader.animation(name=image_name)
    return image


def create_effect_animation(image_name, duration, rows, columns):
    effect_seq = pyglet.image.ImageGrid(loader.image(image_name), rows, columns)
    effect_frames = []
    for row in range(rows, 0, -1):
        end = row * columns
        start = end - (columns -1) -1
        for effect_frame in effect_seq[start:end:1]:
            effect_frames.append(AnimationFrame(effect_frame, duration))

    effect_frames[(rows * columns) -1].duration = None
    return Animation(effect_frames)

#..\\..\\resources\\Effects\\Grids\\
effect_anims = [create_effect_animation('_LPE__Elemental_Burst_by_LexusX2.png', 0.03, 6, 5),
                create_effect_animation('_LPE__Fire_Arrow_by_LexusX2.png', 0.03, 9, 5),
                create_effect_animation('_LPE__Healing_Circle_by_LexusX2.png', 0.1, 10, 5),
                create_effect_animation('_LPE__Flaming_Time_by_LexusX2.png', 0.1, 5, 5),
                create_effect_animation('_LPE__Gale_by_LexusX3.png', 0.1, 8, 5)
                ]

image_frames = (
                'fire_16.png',
                'fire_27.png',
                'fire_32.png',
                'fire_48.png',
                'fire_71.png',
                'fire_85.png',
                'fire_94.png',
                'fire_32.png',
                'fire_27.png',
                'fire_16.png',
                )

gif_name = 'explosion-boom.gif'
gif_name_star = 'Sample24.gif'

class EffectSprite(pyglet.sprite.Sprite):
    def on_animation_end(self):
        self.delete()
        effects.remove(self)


class EffectLoopSprite(pyglet.sprite.Sprite):
    def __init__(self, img , *args, **kwargs):
        super(EffectLoopSprite, self).__init__(img=img, *args, **kwargs)
        self.image_buffer = self.image
        self._animation_ended = False

    def restart(self):
        if self._animation_ended is True:
            self.image = self.image_buffer
            self._animation_ended = False

    def on_animation_end(self):
        self._animation_ended = True
        # self.delete()

#animSpriteLoop = pyglet.sprite.Sprite(create_effect(image_frames, duration=0.3, loop=True))
#animSpriteLoop.position = (0,0)
#animSprite = pyglet.sprite.Sprite(create_effect(image_frames, duration=0.3, loop=False))
#animSprite.position = (animSprite.width, 0)
gifSprite = pyglet.sprite.Sprite(create_effect_animation_by_gif(gif_name_star))
#gifSprite.position = (animSprite.width*2, 0)

boomEffect = EffectLoopSprite(create_effect_animation_by_gif(gif_name_star))
boomEffect.position = (200, 300)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if(pyglet.window.mouse.LEFT == button):
        effect = EffectSprite(effect_anims[use_effect - 1])
        effect.position = (x - effect.width/2, y - effect.height/2)
        effects.append(effect)
        boomEffect.visible = True
        #boomEffect.restart()

@window.event
def on_mouse_release(x, y, button, modifiers):
    if (pyglet.window.mouse.LEFT == button):
        boomEffect.visible = False
        for effect in effects:
            effect.visible = False

@window.event
def on_key_press(symbol, modifiers):
    global use_effect
    if symbol == pyglet.window.key.B:
        pyglet.gl.glClearColor(*black)
    if symbol == pyglet.window.key.W:
        pyglet.gl.glClearColor(*white)
    if symbol == pyglet.window.key._1:
        use_effect = 1
    if symbol == pyglet.window.key._2:
        use_effect = 2
    if symbol == pyglet.window.key._3:
        use_effect = 3
    if symbol == pyglet.window.key._4:
        use_effect = 4
    if symbol == pyglet.window.key._5:
        use_effect = 5
    if symbol == pyglet.window.key._6:
        use_effect = 6


@window.event
def on_draw():
    window.clear()
    # animSprite.draw()
    # animSpriteLoop.draw()
    boomEffect.draw()
    # gifSprite.draw()
    for effect in effects:
        effect.draw()

pyglet.app.run()


"""
w : switch background to white
b : switch background to black
1 - 5 : change particle effect
Left Mouse click : spawn new effect at mouse location
"""