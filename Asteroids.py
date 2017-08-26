import pyglet
from Asteroid.GameMaster import *
from Asteroid.GameScene import *


def init_world():
    DEBUG_MOD = False
    game_scene = GameScene(width=800, height=600, DEBUG_MOD=DEBUG_MOD)
    game_scene.generate_scene()

if __name__ == '__main__':
    init_world()
    pyglet.app.run()
