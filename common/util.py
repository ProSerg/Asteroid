import pyglet, random, math
import resources
from Asteroid.common.Point import Point

def distance(point_1=Point(0,0), point_2=Point(0,0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1.x - point_2.x) ** 2 + (point_1.y - point_2.y) ** 2)

def player_lives(num_icons, sprite, batch=None):
    """Generate sprites for player life icons"""
    player_lives = []
    for i in range(num_icons):
        new_sprite = pyglet.sprite.Sprite(img=resources.player_image,
                                          x=785-i*30, y=585,
                                          batch=batch)
        new_sprite.scale = 0.5
        player_lives.append(new_sprite)
    return player_lives

def generation_point(rect_place, rect_execute):
    random_pos = Point(
        random.randint(rect_place.left, rect_place.right),
        random.randint(rect_place.bottom, rect_place.top)
    )
    while rect_execute.contains(random_pos) is True:
        random_pos = Point(
            random.randint(rect_place.left, rect_place.right),
            random.randint(rect_place.bottom, rect_place.top)
        )
    else:
        pass
    return random_pos



if __name__ == "__main__":
    lst1 = [1,2,3]
    lst2 = [4,5,6]

    lst = [lst1, lst2]

    # listmerge5 = lambda s: reduce(lambda d,el: d.extend(el) or d, s, [])

    # for ls in listmerge5:
    #     print(ls)