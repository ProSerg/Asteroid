from Asteroid.Items.ItemObject import ItemObject
from Asteroid.UserUI import UserUI
from Asteroid.common.Resources import *
from Asteroid.common.Figure import *
from Asteroid.common.Mechanics import *

from pathlib import Path
# Set up a window


class GameMaster(object):
    NUMS_ASTEROIDS = 10
    background = pyglet.graphics.OrderedGroup(0)
    foreground = pyglet.graphics.OrderedGroup(1)
    asteroids = pyglet.graphics.OrderedGroup(2)

    def __init__(self, batch):
        self.batch = batch
        self.user_ui = UserUI(batch=self.batch)
        self.loader = ResourcesLoader()
        self.fabric = Fabric(self.loader, self.batch)
        self.shoot = True
        self.resistance = 0.01


    def make_asteroid(self, x , y, rotation, rotate_speed, thrust ):
        asteroid_sprite = self.fabric.get_sprite(
            name="asteroid_brown.png",
            scale=0.1,
            rotation=90,
            group=self.foreground,
        )

        asteroid_mechanics = AsteroidMechanics(
            resistance=0.0,
            thrust=thrust,
            rotate_speed=rotate_speed,
        )

        asteroid = ItemObject(
            x=x,
            y=y,
            name="Asteroid",
            sprite=asteroid_sprite,
            rotation=rotation,
            mechanic=asteroid_mechanics,
            bounds=Rectangle(width=asteroid_sprite.width, height=asteroid_sprite.height, rotation=0, color=Color.Blue),
        )

        return asteroid


    def make_user_ship(self, x , y, rotation, rotate_speed, thrust ):
        fire_image = [
            "fire_3.png",
            "fire_4.png",
            "fire_6.png",
            "fire_7.png",
            "fire_8.png",
        ]

        sprite = self.fabric.get_sprite(
            name="player_ship.png",
            scale=0.1,
            rotation=90,
            group=self.foreground,
        )

        ship_mechanics = ShipMechanics(
            resistance=self.resistance,
            thrust=thrust,
            rotate_speed=rotate_speed,
        )

        ship = ItemObject(
            x=x,
            y=y,
            name="UserShip",
            sprite=sprite,
            rotation=rotation,
            mechanic=ship_mechanics,
            bounds=Rectangle(width=sprite.width, height=sprite.height, rotation=0, color=Color.Green),
        )

        engine_sprite = self.fabric.get_animation(
            image_names=fire_image, duration=0.2, rotation=90, scale=0.2, group=self.foreground)
        engine_sprite2 = self.fabric.get_animation(
            image_names=fire_image, duration=0.2, rotation=90, scale=0.2, group=self.foreground)

        engine = ItemObject(
            local_x=-7,
            local_y=35,
            name="EngineItem",
            sprite=engine_sprite,
            rotation=0,
            #bounds=Rectangle(width=engine_sprite.width, height=engine_sprite.height, rotation=0, color=Color.Red)
        )

        engine2 = ItemObject(
            local_x=7,
            local_y=35,
            name="EngineItem2",
            sprite=engine_sprite2,
            rotation=0,
            #bounds=Rectangle(width=engine_sprite.width, height=engine_sprite.height, rotation=0, color=Color.Red)
        )

        ship.add(engine)
        ship.add(engine2)
        return ship

    def make_bullet(self, x, y, rotation):
        bullet_sprite = self.fabric.get_sprite(
            name="bullet.png",
            scale=0.8,
            rotation=90,
            group=self.foreground,
        )

        bullet_mechanics = BulletMechanics(
            resistance=0.0,
            thrust=300,
            rotate_speed=1.0,
        )
        bounds = Circle(
            radius=bullet_sprite.width / 2, color=Color.Red ,
            slide_x=(bullet_sprite.height/2 - bullet_sprite.width/2) *0.8, slide_y=00)

        bullet = ItemObject(
            x=x,
            y=y,
            local_x=15,
            local_y=0,
            name="bullet",
            sprite=bullet_sprite,
            rotation=rotation,
            mechanic=bullet_mechanics,
            bounds=bounds,
        )

        return bullet