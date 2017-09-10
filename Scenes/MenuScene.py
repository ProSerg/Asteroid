from Scenes.SceneManager import *
import pyglet

class MenuScene(Scene):
    """Menu scene in progress."""

    def __init__(self):
        super().__init__()
        # Commenting the lines that depend on images.
        # We don't have access to them.

        # self.bg = pyglet.image.load("menu_bg.jpg")
        # self.snake = pyglet.sprite.Sprite ( pyglet.image.load("snake.png") )
        # self.snake.position = 320, 0
        self._status = "menu"
        self.user_chip = TypeShip.FIGHTER

        self._idx_choose = 1

        self._menu = {
            1: TypeShip.FIGHTER,
            2: TypeShip.BUG,
            3: TypeShip.SAUCER,
        }

    def init(self, master, key_handler,  width, height):
        self.key_handler = key_handler
        # background = pyglet.graphics.OrderedGroup(0)
        self.width = width
        self.height = height

        self.batch = pyglet.graphics.Batch()
        self.menu = master.make_menu(self.batch)
        self._label = pyglet.text.Label(
            text='<< ASTROIDE >>',
            x=400, y=550,
            anchor_x='center',
            batch=self.batch,
            group=None)

        self.menu.select_choose(self.user_chip)

    def on_key_press(self, app, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            if self._idx_choose > 1:
                self._idx_choose -= 1
        elif symbol == pyglet.window.key.DOWN:
            if self._idx_choose < 3:
                self._idx_choose += 1

        if symbol == pyglet.window.key._1:
            self._idx_choose = 1
        elif symbol == pyglet.window.key._2:
            self._idx_choose = 2
        elif symbol == pyglet.window.key._3:
            self._idx_choose = 3

        self.user_chip = self._menu[self._idx_choose]
        self.menu.select_choose(self.user_chip)

    def on_key_release(self, app, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self._status = "play"
            app.set_curr_ship(self.user_chip)
            app.changeStatus(self._status)



    def on_step(self, app, dt):
        # print("Step: {}".format(dt))
        pass

    def on_draw(self, manager):
        super().on_draw(manager)
        manager.window.clear()
        self.batch.draw()

        # self.bg.blit(0, 0)
        # self.snake.draw()