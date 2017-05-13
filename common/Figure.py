import math
from enum import Enum
import pyglet
import pyglet.gl as gl
from Asteroid.common.Point import Point
from pyglet.graphics import *

class Color(Enum):
    White = [255,255,255]
    Red = [255,0,0]
    Lime = [ 0,255,0]
    Blue = [0,0,255]
    Yellow = [255,255,0]
    Aqua = [0,255,255]
    Magenta = [255,0,255]
    Silver = [192,192,192]
    Gray = [128,128,128]
    Maroon = [128,0,0]
    Olive = [128,128,0]
    Green = [0,128,0]
    Purple = [128,0,128]
    Teal = [0,128,128]
    Navy = [0,0,128]


class Mode(Enum):
    Line = "line"
    Triangle = "triangle"
    Rectangle = "rectangle"
    Circle = "circle"


class Figure(object):
    def __init__(self, cx=0, cy=0, width=0, height=0, slide_x=0, slide_y=0, num_segments=0, mode=Mode.Line, points=None, color=Color.White):
        # self._cpoint = Point(0,0)
        self._mode = mode
        self._points = points
        self._color = color
        self._width = width
        self._height = height
        self._num_segments = num_segments

        self._slide_x = slide_x
        self._slide_y = slide_y

        self.cx = cx
        self.cy = cy

    def _set_num_segments(self, num_segments):
        self._num_segments = num_segments

    def _get_num_segments(self):
        return self._num_segments

    num_segments = property(_get_num_segments, _set_num_segments)

    def _set_width(self, width):
        self._width = width

    width = property(lambda self: self._width, _set_width)

    def _set_height(self, height):
        self._height = height

    height = property(lambda self: self._height, _set_height)

    def _set_cx(self, x):
        self._cx = x

    cx = property(lambda self: self._cx, _set_cx)

    def _set_cy(self, y):
        self._cy = y

    cy = property(lambda self: self._cy, _set_cy)

    def _set_slide_x(self, x):
        self._slide_x = x

    slide_x = property(lambda self: self._slide_x, _set_slide_x)

    def _set_slide_y(self, y):
        self._slide_y = y

    slide_y = property(lambda self: self._slide_y, _set_slide_y)

    def _set_center(self, cpoint):
        self._cx = cpoint.x
        self._cy = cpoint.y

    center = property(lambda self: Point(self._cx, self._cy), _set_center)

    def _set_mode(self, mode):
        self._mode = mode

    mode = property(lambda self: self._mode, _set_mode)

    def _set_points(self, points):
        if type(points) is not list:
            raise Exception("Point is not list")
        self._points = points

    points = property(lambda self: self._points, _set_points)

    def _set_color(self, color):
        self._color = color

    color = property(lambda self: self._color, _set_color)

    def _get_vertex(self, count, points, colors):
        return pyglet.graphics.vertex_list(count,
            ('v2f', points),
            ('c3B', colors)
        )


    def move(self, dx, dy):
        for point in self.points:
            point.slide_xy(dx, dy)

    def vertex(self):
        raise Exception("Function needs realising")

    def draw(self):
        raise Exception("Function needs realising")


class Circle(Figure):
    def __init__(self, radius, *args, **kwargs):
        super(Circle, self).__init__(
            mode=Mode.Circle,
            points=[],
            width=radius,
            height=radius,
            num_segments=100,
            *args, **kwargs)
        self._radius = radius
        self.make()

    def get_center(self, rotation):
        r = -math.radians(rotation)
        cr = math.cos(r)
        sr = math.sin(r)
        return Point(
            ( self.cx ) * cr - ( self.cy ) * sr,
            ( self.cx ) * sr + ( self.cy ) * cr)

    def _get_radius(self):
        return self._radius

    def _set_radius(self, radius):
        self._radius = radius

    radius = property(_get_radius, _set_radius)

    def make(self, rotation=0, x=0, y=0):
        self.points[:] = []
        cpoint = self.get_center(rotation)
        dx = cpoint.x + x
        dy = cpoint.y + y
        for ii in range(self.num_segments):
            theta = 2.0 * math.pi * float(ii) / float(self.num_segments)
            px = self.radius * math.cos(theta)
            py = self.radius * math.sin(theta)
            self.points.append(Point(px + dx, py + dy))

    def vertex(self):
        points = []
        colors = []

        for point in self.points:
            points.append(point.x)
            points.append(point.y)

        for idx in range(self.num_segments):
            for color in self._color.value:
                colors.append(color)
        try:
            vertex = self._get_vertex(self.num_segments, points, colors)
        except Exception as ex:
            print("%s.Vertex: %s" % (self.__class__.__name__, ex))
        else:
            return vertex

    def draw(self):
        self.vertex().draw(GL_LINE_LOOP)

class Rectangle(Figure):

    def __init__(self, width=0, height=0, rotation=0, *args, **kwargs):
        super(Rectangle, self).__init__(mode=Mode.Rectangle, points=[], num_segments=4,
            *args, **kwargs)
        self._width = width
        self._height = height
        self._rotation = rotation
        self.vec2d = [
            Point(-self.width/2, -self.height/2),
            Point(self.width/2, -self.height/2),
            Point(self.width/2, self.height/2),
            Point(-self.width/2, self.height/2),
        ]
        self.make()

    def make(self):
        self.points[:] = []
        for vec in self.vec2d:
            r = -math.radians(self.rotation)
            cr = math.cos(r)
            sr = math.sin(r)
            dx = vec.x * cr - vec.y * sr + self.cx
            dy = vec.x * sr + vec.y * cr + self.cy
            self.points.append(Point(dx, dy))

    def _set_rotation(self, rotation):
        self._rotation = rotation

    rotation = property(lambda self: self._rotation, _set_rotation)

    def rotate(self, theta):
        delta = self.rotation - theta
        if delta != 0.0:
            self.rotation = theta
            self.make()

    def vertex(self):
        points = []
        colors = []

        for point in self.points:
            points.append(point.x)
            points.append(point.y)

        for idx in range(self.num_segments):
            for color in self._color.value:
                colors.append(color)
        try:
            vertex = self._get_vertex(self.num_segments, points, colors)
        except Exception as ex:
            print("%s.Vertex: %s" % (self.__class__.__name__, ex))
        else:
            return vertex

    def draw(self):
        self.vertex().draw(GL_LINE_LOOP)


if __name__ == "__main__":
    x = 0
    y = 0
    width = 2
    height = 2
    figure = Circle(
        cx=x - width / 2,
        cy=y - height / 2,
        color=Color.Green,
        radius=width,
    )
    print(figure.points)
    print(figure.vertex())
    # rect.rotate(45)
    # print(rect.points)