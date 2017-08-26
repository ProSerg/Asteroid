from Asteroid.common.AnimationManager import *
from Asteroid.common.Resources import *


window = pyglet.window.Window()

white = (1, 1, 1, 1)
black = (0, 0, 0, 1)
pyglet.gl.glClearColor(*black)

effects = []
use_effect = 1

resource_paths = [
    "../../resources/Fires",
    "../../resources/Effects/Grids",
    "../../resources/Effects/Blue Effects",
    "../../resources/Blue/",
    "../../resources/Animations/gif/",
]

gif_name = 'explosion-boom.gif'
gif_name_star = 'Sample24.gif'
blue_effects = [
    "1_0.png",
    "1_1.png",
    "1_2.png",
    "1_3.png",
    "1_4.png",
    "1_5.png",
    "1_6.png",
    "1_7.png",
    "1_8.png",
    "1_9.png",
    "1_10.png",
    "1_11.png",
    "1_12.png",
    "1_13.png",
    "1_14.png",
    "1_15.png",
    "1_16.png"
]

loader = ResourcesLoader(resource_paths)

anim_manager = AnimationManager(loader=loader, batch=pyglet.graphics.Batch())

anim_manager.createSpringEffect(name="portal", img="_LPE__Healing_Circle_by_LexusX2.png", scale=.6,
                                type_image="grid", inverse=True, duration=0.03, rows=10, columns=5, rotation=0)

anim_manager.createSpringEffect(name="effect", img=gif_name, scale=1.0, type_image="gif")

anim_manager.createSpringEffect(name="boom", img="boom_grid.png", scale=1.0, type_image="grid",
                                duration=0.03, rows=4, columns=8, rotation=0)

anim_manager.createSpringEffect(name="greenboom", img="_LPE__Elemental_Burst_by_LexusX2.png", scale=.6,
                                type_image="grid", duration=0.03, rows=6, columns=5, rotation=0)

anim_manager.createSpringEffect(name="boom2", img="explosion_01_strip13.png", scale=0.8,
                                type_image="grid", duration=0.05, rows=1, columns=13, rotation=0)

anim_manager.createSpringEffect(name="boom3", img="explosion_03_strip13.png", scale=0.8,
                                type_image="grid", duration=0.05, rows=1, columns=13, rotation=0)

anim_manager.createSpringEffect(name="blue", img=blue_effects, scale=0.5,
                                type_image="frames", duration=0.02, rotation=0, looped=False, anchor_x=0, anchor_y=0)

names = ["none", "boom", "greenboom", "boom2" , "boom3", "blue", "portal"]

@window.event
def on_mouse_press(x, y, button, modifiers):
    if(pyglet.window.mouse.LEFT == button):
        # effect.position = ()
        anim_manager.playAnimation(names[use_effect], x, y)
        # boomEffect.visible = True
        #boomEffect.restart()



@window.event
def on_mouse_release(x, y, button, modifiers):
    if (pyglet.window.mouse.LEFT == button):
        pass
        # boomEffect.visible = False
        # for effect in effects:
        #     effect.visible = False

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
    # boomEffect.draw()
    # gifSprite.draw()
    anim_manager.Play()


if __name__ == "__main__":
    pyglet.app.run()

"""
w : switch background to white
b : switch background to black
1 - 5 : change particle effect
Left Mouse click : spawn new effect at mouse location
"""