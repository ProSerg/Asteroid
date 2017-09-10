from Scenes.SceneManager import *

class GameScene(Scene):
    def __int__(self, batch):
        super().__init__()
        # self._batch = batch

    def init(self, master, width, height):
        self.key_handler = key.KeyStateHandler()
        # background = pyglet.graphics.OrderedGroup(0)
        self.width = width
        self.height = height
        ##
        self.items = set()
        self.bullets = []
        self.stars = []
        ##

        self.master = master
        self.loader = master.loader
        self.batch = pyglet.graphics.Batch()
        self.background = master.createBackGround(self.batch)
        self._start_ship_position = Point(400, 350)
        self._type_user_ship = None
        self.user_ship = None
        self.running = False

        self._ships = 4
        self._score = 0
        self._bonus = 0

        self.user_ui = self.master.make_game_ui(
            self.batch)

        self.master.make_star(-50, -50, self.batch, TypeAsteroid.MEDIUM)
        self.master.make_star(-50, -50, self.batch, TypeAsteroid.BIG)
        self.master.make_star(-50, -50, self.batch, TypeAsteroid.SMALL)

    def arrivalShip(self):
        self.master.play(
            "portal", self._start_ship_position.x,
            self._start_ship_position.y,
            batch=self.batch,
            group=self.loader.effects)

        self.user_ship.update_pos(
            x=self._start_ship_position.x,
            y=self._start_ship_position.y,
        )

        self.add_item(self.user_ship)

        self.user_ship.visible(True)
        self._ships -= 1

    def leavingShip(self):
        self.master.play(
            "portal", self.user_ship.sprite.x, self.user_ship.sprite.y,
            batch=self.batch, group=self.loader.effects)
        self.user_ship.visible(False)
        self.del_item(self.user_ship)
        self._ships += 1

    def start(self, ship):
        self._type_user_ship = ship

        self.user_ship = self.master.make_user_ship(
            x=self._start_ship_position.x,
            y=self._start_ship_position.y,
            key_handler=self.key_handler,
            batch=self.batch,
            type_ship=self._type_user_ship)

        self.user_ship.visible(False)

        self.user_ui.setShip(self._type_user_ship.value)

        # self.push_handlers(self.user_ship.mechanic.key_handler)

        self.arrivalShip()
        self.running = True

    def restartGame(self):
        self._score = 0
        self._bonus = 0
        self._ships = 4

        self.user_ship.visible(False)
        self.del_item(self.user_ship)

        while self.items:
            item = self.items.pop()
            item.destroy()

        while self.stars:
            bonus = self.stars.pop()
            bonus.destroy()
            del bonus

        self.user_ship.live = False
        self.user_ship.destroy()



    def create_wave(self, numbers=7):
        for num in range(numbers):
            asteroid = self.master.generate_asteroid(
                name="Asteroid_{}".format(num),
                x=random.randint(50, 800),
                y=random.randint(700, 750),
                batch=self.batch)
            self.add_item(asteroid)

    def usePortal(self):
        if self._ships > 0:
            if self.user_ship.live is False:
                print("self.user_ship.live : {}".format(self.user_ship.live))
                self.user_ship.reset()
                self.arrivalShip()

    def stop(self):
        self.running = False

    def _get_objects(self):
        return self.items

    def check_bounds(self, item):
        """Use the classic Asteroids screen wrapping behavior"""
        figure = item.bounds
        if figure is not None:
            x = item.x
            y = item.y
            min_x = -figure.width / 2
            min_y = -figure.height / 2
            max_x = self.width + figure.width / 2
            max_y = self.height + figure.height / 2
            flag = False
            if x < min_x:
                 x = max_x
                 flag = True
            elif x > max_x:
                 x = min_x
                 flag = True
            if y < min_y:
                 y = max_y
                 flag = True
            elif y > max_y:
                 y = min_y
                 flag = True
            if flag is True:
                item.update_pos(x, y)

    def moving(self, _dt):
        for obj in self._get_objects():
            if obj.static is False:
                obj.update(_dt)

        for bullet in self.bullets:
            bullet.update(_dt)

    def check_collision(self, obj1, obj2):
        if obj2 == obj1:
            return False
        else:
            if (obj1.x < obj2.x + obj2.bounds.width) \
                and (obj2.x < obj1.x + obj1.bounds.width) \
                and (obj1.y < obj2.y + obj2.bounds.height) \
                and (obj2.y < obj1.y + obj1.bounds.height):
                return True
            else:
                return False

    def check_hit(self, bullet, asteroid):
        rx = asteroid.x - asteroid.bounds.width / 2
        ry = asteroid.y - asteroid.bounds.height / 2
        width = asteroid.bounds.width
        height = asteroid.bounds.height
        cx = bullet.x
        cy = bullet.y
        radius = bullet.bounds.radius
        return self.isCircleToRect(cx, cy, radius, rx, ry, width, height)

    def isCircleToRect(self, cx, cy, radius, rx, ry, width, height):
        x = cx
        y = cy

        if cx < rx:
            x = rx
        elif cx > (rx + width):
            x = rx + width

        if cy < ry:
            y = ry
        elif cy > (ry + height):
            y = ry + height

        return ((cx - x) * (cx - x) + (cy - y) * (cy - y)) <= (radius * radius)


    def processing_collisions(self):
        '''
        Обработчик столкновений определяет если были столкновений, то взависимости что с чем столкнулось
        получет повредждения. А также вектор визического удара.
        :return:
        '''
        objects = self._get_objects()
        for obj in objects:
            if obj.static is False:
                self.check_bounds(obj)

        for obj in self.bullets:
            if obj.static is False:
                self.check_bounds(obj)

        # for i in range(len(objects)):
        #     for j in range(i + 1, len(objects)):
        #         self.check_collision(objects[i], objects[j])
        flag = False
        for obj in objects.copy():
            if obj.typeItem == TypeItem.ASTEROID:
                if self.check_collision(self.user_ship, obj) is True:
                    self.user_ship.mechanic.add_damage(value=obj.mechanic.damage)
                for bullet in self.bullets:
                    if self.check_hit(bullet, obj) is True:
                        # obj.bounds.color = Color.Red
                        if obj.mechanic.live > 0:
                            obj.mechanic.add_damage(value=bullet.mechanic.damage)
                            bullet.mechanic.destroy()

        for star in self.stars:
            if self.check_collision(self.user_ship, star) is True:
                self._score += star.mechanic.bonus
                star.mechanic.destroy()
                star.mechanic.used = True

    def processing_objects(self, dt):
        '''
        Обработчик объектов. Проверяет состояние параметров. Например, проверяет если у объекта закончились жизни, то
        уничтожает. Или получил повреждения, то вычитает.
        :return:
        '''
        objects = self._get_objects()
        for obj in objects.copy():
            if obj.typeItem == TypeItem.ASTEROID:
                obj.process(dt)
                if obj.live is False:
                    self.master.play(
                        "asteroid_boom",
                        obj.sprite.x, obj.sprite.y,
                        batch=self.batch, group=self.loader.effects)
                    splinters = self.master.generate_splinters(obj, self.batch)
                    for item in splinters:
                        self.add_item(item)
                    self.stars.append(self.master.make_star(
                        x=obj.sprite.x,
                        y=obj.sprite.y,
                        batch=self.batch,
                        type=obj.mechanic.typeAsteroid))
                    self.del_item(obj)
                    obj.destroy()
                    del obj
                    obj = None
            else:
                self.user_ship.process(dt)
                if self.user_ship.live is False:
                    self.user_ship.visible(False)
                    self.master.play(
                        "ship_boom",
                        self.user_ship.sprite.x, self.user_ship.sprite.y,
                        batch=self.batch, group=self.loader.effects)
                    self.del_item(self.user_ship)
                else:
                    bullet = self.user_ship.mechanic.shot(
                        self.user_ship.x,
                        self.user_ship.y,
                        self.batch)
                    if bullet:
                        self.add_bullet(bullet)

        for obj in self.bullets:
            obj.process(dt)
            if obj.live is False:
                if obj.mechanic.boom is True:
                    self.master.play(
                        "bullet_boom",
                        obj.sprite.x, obj.sprite.y,
                        batch=self.batch, group=self.loader.effects)
                self.bullets.remove(obj)
                del obj
                obj = None

        for star in self.stars:
            star.process(dt)
            if star.mechanic.is_live() is False:
                if star.mechanic.used is False:
                    self.master.play(
                        "star_boom",
                        star.sprite.x + 25, star.sprite.y + 25,
                        batch=self.batch, group=self.loader.effects)
                self.stars.remove(star)
                star.destroy()
                del star
                star = None

    def processing_environment(self):
        self.user_ui.update_score(self._score)
        self.user_ui.update_ammo(self.user_ship.mechanic.getAmmo())
        self.user_ui.update_energy(self.user_ship.mechanic.getEnergy())
        self.user_ui.update_live(self._ships)

    def on_step(self, app, dt):
        self.moving(dt)
        self.processing_collisions()
        self.processing_objects(dt)
        self.processing_environment()

    def on_mouse_press(self, app, x, y, button, modifiers):
        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, app, x, y, button, modifiers):
        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, app, x, y, dx, dy):
        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, app, x, y, dx, dy, buttons, modifiers):
        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_key_press(self, app, symbol, modifiers):
        self.key_handler.on_key_press(symbol, modifiers)

        if symbol == pyglet.window.key.SPACE:
            self.usePortal()
        elif symbol == pyglet.window.key.R:
            self.usePortal()
            self.create_wave()
        elif symbol == pyglet.window.key.ESCAPE:
            # self.clear_wave()
            # self.restartGame()
            pass

        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_key_press(symbol, modifiers)

    def on_key_release(self, app, symbol, modifiers):
        self.key_handler.on_key_release(symbol, modifiers)

        if symbol == pyglet.window.key.F10:
            self.restartGame()
            self._status = "menu"
            app.changeStatus(self._status)

        if self.user_ship.getVisible() is True:
            self.user_ship.mechanic.on_key_release(symbol, modifiers)



    def on_draw(self, manager):
        super().on_draw(manager)
        manager.window.clear()
        self.batch.draw()

    # proccessing game mechanics

    def del_item(self, item):
        try:
            self.items.remove(item)
        except KeyError as ex:
            pass

    def add_item(self, item):
        self.items.add(item)

    def add_bullet(self, bullet):
        if type(bullet) is list:
            self.bullets.extend(bullet)
        else:
            self.bullets.append(bullet)
