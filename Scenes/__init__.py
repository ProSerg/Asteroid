from Scenes.SceneManager import *
from Scenes.MenuScene import *
from Scenes.GameScene import *

if __name__ == '__main__':
    scens = {
        "menu": MenuScene(),
        "game": GameScene()
    }

    SceneManager("menu", scens, show_fps=True)
    pyglet.app.run()