import pyglet
from pyglet.resource import Loader
from pyglet.image import Animation, AnimationFrame

resources_paths = [
    "../../resources/Effects/Fires",
    "../../resources/Effects/Grids",
]

fire_image_start = [
    "fire_1.png",
    "fire_2.png",
    "fire_3.png",
]

fire_image_end = [
    "fire_3.png",
    "fire_2.png",
    "fire_1.png",
    "fire_0.png",
    "fire_none.png",
]

fire_image = [
    "fire_3.png",
    "fire_4.png",
    "fire_6.png",
    "fire_7.png",
    "fire_8.png",
]
effects = []

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

def create_effect_animation(self, image_name, columns, rows):
    effect_seq = pyglet.image.ImageGrid(pyglet.image.load(image_name), rows, columns)
    effect_frames = []
    for row in range(rows, 0, -1):
        end = row * columns
        start = end - (columns -1) -1
        for effect_frame in effect_seq[start:end:1]:
            effect_frames.append(AnimationFrame(effect_frame, 0.1))

    effect_frames[(rows * columns) -1].duration = None
    return Animation(effect_frames)


def create_effect_animation(image_name, duration, brow, rows, column, columns):
    effect_seq = pyglet.image.ImageGrid(loader.image(image_name), rows, columns)
    effect_frames = []
    end = brow * columns
    start = end - (columns - 1)
    for effect_frame in effect_seq[start:end:1]:
        effect_frames.append(AnimationFrame(effect_frame, duration))

    # effect_frames[((rows-brow) * (columns -column) ) -1].duration = None
    return Animation(effect_frames)

# The main pyglet window with OpenGL context
# w = animSprite.width
# h = animSprite.height

win = pyglet.window.Window(300,300)
# Set window background color to white.
pyglet.gl.glClearColor(1, 1, 1, 1)

animSprite = pyglet.sprite.Sprite(create_effect(fire_image, duration=0.3, loop=True))

fire_flush = create_effect_animation('sparks.png', 1, 1, 6, 0, 4)
animGridSprite = pyglet.sprite.Sprite(fire_flush)
effects.append(animSprite)
animSprite.visible = False


@win.event
def on_key_press(symbol, modifiers):
    global use_effect
    if symbol == pyglet.window.key.W:
        animSprite.visible = True

    if symbol == pyglet.window.key.E:
        pass

@win.event
def on_key_release(symbol, modifiers):
    global use_effect
    if symbol == pyglet.window.key.W:
        animSpriteStop = pyglet.sprite.Sprite(create_effect(fire_image_end, duration=0.3, loop=False))
        effects.append(animSpriteStop)
        animSprite.visible = False


# The @win.event is a decorator that helps modify the API
# methods such as
# on_draw called when draw event occurs.
@win.event
def on_draw():
    win.clear()
    animGridSprite.draw()
    for effect in effects:
        effect.draw()

pyglet.app.run()