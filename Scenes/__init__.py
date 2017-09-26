from Asteroid.settings.GameSettings import *
from Scenes.GameScene import *
from Scenes.MenuScene import *
from Scenes.SceneManager import *

#TODO
#3. Next Wave
#4. End Game
#6. Light refactoring
#7. CI/CD
#8. AutoTest

if __name__ == '__main__':
    scens = {
        "menu": MenuScene(),
        "game": GameScene()
    }
    settings = GameSettings()
    SceneManager("menu", scens, settings)
    pyglet.app.run()