import pyglet, math
from Asteroid.common.Point import Point

# TODO MAX SPEED
class ItemObject(object):

    _sprite = None
    _bounds = None
    _mechanic = None
    def __init__(self,
                 name,
                 x=0,
                 y=0,
                 local_x=0,
                 local_y=0,
                 rotation=0,
                 static=False,
                 bounds=None,
                 childs=None,
                 parent=None,
                 sprite=None,
                 mechanic=None,
                 ):
        self._name = name
        self._x = x
        self._y = y
        self._live = True
        self._local_x = local_x
        self._local_y = local_y
        self._local_point = Point(local_x, local_y)
        self._rotation = rotation

        self.sprite = sprite
        self.bounds = bounds
        self.mechanic = mechanic
        if self.mechanic:
            self.mechanic.rotation = self._rotation
        if childs:
            self._childs = childs
        else:
            self._childs = []
        self._parent = parent
        self._static = static

    def _get_name(self):
        return self._name

    def _set_name(self, name):
        self._name = name

    name = property(_get_name, _set_name, doc="""FIXME""")

    def _get_live(self):
        return self._live

    def _set_live(self, live):
        self._live = live

    live = property(_get_live, _set_live, doc="""FIXME""")

    def _get_static(self):
        return self._static

    def _set_static(self, static):
        self._static = static

    static = property(_get_static, _set_static, doc="""FIXME""")

    def _get_parent(self):
        return self._parent

    def _set_parent(self, parent):
        self._parent = parent

    parent = property(_get_parent, _set_parent, doc="""FIXME""")

    def _get_x(self):
        return self._x

    def _set_x(self, x):
        self._x = x

    x = property(_get_x, _set_x, doc="""FIXME""")

    def _get_y(self):
        return self._y

    def _set_y(self, y):
        self._y = y

    y = property(_get_y, _set_y, doc="""FIXME""")

    def _get_local_point(self):
        return Point(self._local_x, self._local_y)

    def _set_local_point(self, point):
        if type(point) == Point:
            self._local_x = point.x
            self._local_y = point.y
        else:
            raise Exception("the function uses Point")

    local_point = property(_get_local_point, _set_local_point, doc="""FIXME""")

    def _get_rotation(self):
        return self._rotation

    def _set_rotation(self, theate):
        self._rotation = theate

    rotation = property(_get_rotation, _set_rotation, doc="""FIXME""")

    def _get_bounds(self):
        return self._bounds

    def _set_bounds(self, bounds):
        self._bounds = bounds
        if self._bounds:
            r = -math.radians(self.rotation)
            cr = math.cos(r)
            sr = math.sin(r)
            d_x = self.local_point.x + self.bounds.slide_x
            d_y = self.local_point.y + self.bounds.slide_y
            self._bounds.rotation = self.sprite.rotation
            self._bounds.center = Point(
                d_x * cr - d_y * sr + self.x,
                d_x * sr + d_y * cr + self.y)
            self._bounds.make()

    bounds = property(_get_bounds, _set_bounds, doc="""FIXME""")

    def _get_mechanic(self):
        return self._mechanic

    def _set_mechanic(self, mechanic):
        self._mechanic = mechanic
        if self._mechanic:
            self._mechanic.rotation = self.rotation

    mechanic = property(_get_mechanic, _set_mechanic, doc="""FIXME""")

    def _get_sprite(self):
        return self._sprite

    def _set_sprite(self, sprite):
        self._sprite = sprite
        if self._sprite:
            r = -math.radians(self.rotation)
            cr = math.cos(r)
            sr = math.sin(r)
            d_x = self.local_point.x
            d_y = self.local_point.y
            self._sprite.x = d_x * cr - d_y * sr + self.x
            self._sprite.y = d_x * sr + d_y * cr + self.y
            self._sprite.rotation += self.rotation

    sprite = property(_get_sprite, _set_sprite, doc="""FIXME""")

    def visible(self, flag):
        self.sprite.visible = flag
        for child in self.childs():
            child.sprite.visible = flag

    def getVisible(self):
        return self.sprite.visible

    def draw(self):
        """
        перерисовываем объект
        :return:
        """
        try:
            # self.sprite.draw() не нужно рисовать поскольку есть batch
            self.bounds.draw()
        except Exception as ex:
            #print(self.bounds)
            pass

        try:
            for image in self.childs():
                image.draw()
        except Exception as ex:
            print(ex)


    def set_rotation(self, rotate):
        self.rotation = rotate
        if self.sprite:
            self.sprite.rotation = rotate
        if self.bounds:
            self.bounds.rotation = rotate
            self.bounds.make()

    def set_position(self, x, y):
        dx = self.local_point.x
        dy = self.local_point.y

        r = -math.radians(self.rotation)
        cr = math.cos(r)
        sr = math.sin(r)

        self.x = x
        self.y = y
        if self.sprite:
            d_x = self.local_point.x
            d_y = self.local_point.y
            self.sprite.x = d_x * cr - d_y * sr + self.x
            self.sprite.y = d_x * sr + d_y * cr + self.y

        if self._bounds:
           d_x = self.local_point.x + self.bounds.slide_x
           d_y = self.local_point.y + self.bounds.slide_y
           self._bounds.center = Point(
               d_x * cr - d_y * sr + self.x,
               d_x * sr + d_y * cr + self.y)
           self._bounds.make()


        for item in self.childs():
            item.set_position(x, y)

    def turn(self, theata, dt):
        x0 = self.x
        y0 = self.y
        self.move( -x0, -y0, 0)
        r = -math.radians(theata)
        cr = math.cos(r)
        sr = math.sin(r)

        # dx = (self.sprite.x ) * cr - (self.sprite.y ) * sr
        # dy = (self.sprite.x ) * sr + (self.sprite.y ) * cr


        if self.sprite:
            d_x = self.sprite.x
            d_y = self.sprite.y
            self.sprite.x = d_x * cr - d_y * sr + self.x
            self.sprite.y = d_x * sr + d_y * cr + self.y
            # self.sprite.rotation = theata
            # self.sprite.x = dx
            # self.sprite.y = dy

        if self.bounds:
            d_x = self.local_point.x + self.bounds.slide_x
            d_y = self.local_point.y + self.bounds.slide_y
            self._bounds.center = Point(
                d_x * cr - d_y * sr + self.x,
                d_x * sr + d_y * cr + self.y)
            self._bounds.make()
            # self.bounds.cx = dx
            # self.bounds.cy = dy

        self.move(x0, y0, 0)

    def move(self, dx=0, dy=0, da=0.0 ):
        """
        переместить объект на значения.
        :param dx:
        :param dy:
        :param da:
        :return:
        """
        self.x += dx
        self.y += dy
        self.rotation += da
        if self.rotation > 360:
            self.rotation -= 360

        if self.sprite:
            self.sprite.x += dx
            self.sprite.y += dy
            self.sprite.rotation += da
            if self.sprite.rotation > 360:
               self.sprite.rotation -= 360

        if self.bounds:
            self.bounds.cx += dx
            self.bounds.cy += dy
            self.bounds.rotation += da
            if self.bounds.rotation > 360:
                self.bounds.rotation -= 360
            self.bounds.make()

    def process(self):
        """
        производим действия над объектом как резудльтат
        событий в игровом мире : столкнавения, попадания и др.
        :return:
        """
        if self.mechanic:
            self.mechanic.process_live()
            self.live = self.mechanic.is_live()


    def update(self, dt):
        """
        обновляем положение объекта в игровом миоре
        :param dt:
        :return:
        """
        if self.mechanic:
            self.mechanic.update(dt)
            dx = self.mechanic.dx
            dy = self.mechanic.dy
            da = self.mechanic.da
        else:
            dx = dy = da = 0

        self.move(dx, dy, da)
        for item in self.childs():
            # pass
            # item.update(dt)
            item.move(dx, dy, da)
            item.turn(da, dt)

    def update_pos(self, x, y):
        self.set_position(x, y)
        for item in self.childs():
            item.turn(-90, 1)

    def add(self, item):
        item.parent = self
        item.set_position(self.x, self.y)
        item.move(da=self.rotation)
        item.turn(self.rotation + 270, 1)
        self._childs.append(item)

    def remove(self, item):
        pass

    def childs(self):
        return self._childs

    def reset(self):
        self.mechanic.reset()

    def destroy(self):
        for child in self.childs():
           child.destroy()
        self.sprite.delete()


