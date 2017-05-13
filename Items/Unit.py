from Asteroid.Items.ItemObject import ItemObject
from Asteroid.common.Point import Point
from Asteroid.common.Rect import Rect
import queue



class Unit(ItemObject):
    def __init__(self,
                 rotation=0.0,
                 figure=None,
                 items=None,
                 user_drive=False,
                 *args, **kwargs):
        super(Unit, self).__init__(*args, **kwargs)
        self._items = items
        self._figure = figure
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.velocity_angle = 0.0
        self._rotation = rotation
        self._user_drive = user_drive
        self._collision_obj = queue.Queue()


        try:
            for item in self._items:
                item.set_position(self.x + item.local_point.x, self.y + item.local_point.y)
                item.rotation = rotation
        except Exception as ex:
            self._items = []

    def is_user_drive(self):
        return self._user_drive

    def _set_rotation(self, rotation):
        self._rotation = rotation
        # for item in self._items:
        #     item.rotation = rotation

    rotation = property(lambda self: self._rotation, _set_rotation,
                        doc='''Clockwise rotation of the sprites, in degrees.
    :type: float
    ''')

    def _set_figure(self, figure):
        self._figure = figure

    def _get_figure(self):
        return self._figure

    figure = property(_get_figure, _set_figure)

    def get_center(self):
        cpoint = self.figure.get_center(self.rotation)
        return Point(self.x + cpoint.x, self.y + cpoint.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        for item in self._items:
            item.x = self.x
            item.y = self.y

    def add_item(self, item):
        item.x = self.x + item.local_point.x
        item.y = self.y + item.local_point.y
        self._items.append(item)

    def get_items(self):
        return self._items

    # static = property(get_items, add_item, doc="FIXME")


    def update(self, dt):
        dx = self.velocity_x * dt
        dy = self.velocity_y * dt
        self.x += dx
        self.y += dy
        for item in self._items:
            item.x += dx
            item.y += dy
            item.rotation += self.velocity_angle

        if self._figure is not None:
            self._figure.make(self.rotation, x=self.x, y=self.y)

    def draw(self):
        for item in self._items:
            item.draw()
        super(Unit, self).draw()

    def delete(self):
        for item in self._items:
            item.delete()
        super(Unit, self).delete()


    def add_collision_obj(self, obj):
        self._collision_obj.put(obj)

    def process(self):
        while not self._collision_obj.empty():
            self._collision_obj.get()