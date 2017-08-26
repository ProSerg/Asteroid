class Collisions(object):
    def __init__(self):
        pass

    def isCollision(self, unit1, unit2):
        unit1.bounds()
        unit2.bounds()


    def _isCircleToRect(self, cx, cy, radius, rx, ry, width, height):
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