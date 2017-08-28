from Asteroid.Items.ItemObject import ItemObject
from Asteroid.UserUI import UserUI
from Asteroid.common.Figure import *
from Asteroid.common.Mechanics import *
from Asteroid.common.Collisions import *
from Asteroid.common.UnitManager import *
from Asteroid.common.AnimationManager import *

from pathlib import Path
# Set up a window


class GameMaster(object):
    NUMS_ASTEROIDS = 10

    def __init__(self, loader, batch):
        self._loader = loader
        self.batch = batch
        self.user_ui = UserUI(batch=self.batch)

        self.unit_manager = UnitManager(self._loader, self.batch)
        self.anim_manager = AnimationManager(self._loader, self.batch)

        self.anim_manager.createSpringEffect(
            name="asteroid_boom",
            img="explosion_01_strip13.png",
            scale=.8, type_image="grid", duration=0.05, rotation=0, rows=1, columns=13)

        self.anim_manager.createSpringEffect(
            name="ship_boom",
            img="explosion_03_strip13.png",
            scale=.8, type_image="grid", duration=0.05, rotation=0, rows=1, columns=13)

        self.anim_manager.createSpringEffect(
            name="portal",
            img="_LPE__Healing_Circle_by_LexusX2.png",
            scale=.6, type_image="grid", inverse=True, duration=0.015, rows=10, columns=5, rotation=0)

        blue_effects = [
            "1_0.png",
            "1_1.png",
            "1_2.png",
            "1_3.png",
            "1_4.png",
            "1_5.png",
            "1_6.png",
            "1_7.png",
            "1_8.png",
            "1_9.png",
            "1_10.png",
            "1_11.png",
            "1_12.png",
            "1_13.png",
            "1_14.png",
            "1_15.png",
            "1_16.png"
        ]
        self.anim_manager.createSpringEffect(name="bullet_boom", img=blue_effects, scale=0.5,
                                        type_image="frames", duration=0.02, rotation=0, looped=False,
                                        anchor_x=0, anchor_y=0)

        self.shoot = True
        self.resistance = 0.015


    def play(self, name, x, y,  rotation=0, group=None): # FIXME rotation must be  eq 0 only
        self.anim_manager.playAnimation(name, x, y, rotation, group=group)

    def createAnimation(self,name, x, y,  rotation=0, group=None ):
        return self.anim_manager.createAnimation(name, x, y, rotation, group=group)

    def make_asteroid(self, name, x , y, rotation, rotate_speed, thrust ):
        asteroid_sprite = self.unit_manager.get_sprite(
            name="asteroid_brown.png",
            scale=0.1,
            rotation=90,
            group=self._loader.asteroids_group,
        )

        asteroid_mechanics = AsteroidMechanics(
            resistance=0.0,
            thrust=thrust,
            rotate_speed=rotate_speed,
        )

        asteroid = ItemObject(
            x=x,
            y=y,
            name=name,
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

        sprite = self.unit_manager.get_sprite(
            name="player_ship.png",
            scale=0.1,
            rotation=90,
            group=self._loader.ship_group,
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

        engine_sprite = self.anim_manager.getSpringEffect(
            img=fire_image, type_image="frames", group=self._loader.foreground, scale=0.2,
            looped=True, duration=0.2, rotation=90)
        engine_sprite2 = self.anim_manager.getSpringEffect(
            img=fire_image, type_image="frames", group=self._loader.foreground, scale=0.2,
            looped=True, duration=0.2, rotation=90)

        engine = ItemObject(
            local_x=10,
            local_y=40,
            name="EngineItem",
            sprite=engine_sprite,
            rotation=0,
            #bounds=Rectangle(width=engine_sprite.width, height=engine_sprite.height, rotation=0, color=Color.Red)
        )

        engine2 = ItemObject(
            local_x=0,
            local_y=40,
            name="EngineItem2",
            sprite=engine_sprite2,
            rotation=0,
            #bounds=Rectangle(width=engine_sprite.width, height=engine_sprite.height, rotation=0, color=Color.Red)
        )

        ship.add(engine)
        ship.add(engine2)
        return ship

    def make_bullet(self, x, y, rotation, power):
        bullet_sprite = self.unit_manager.get_sprite(
            name="bullet.png",
            scale=0.3,
            rotation=90,
            group=self._loader.effects,
        )

        bullet_mechanics = BulletMechanics(
            resistance=0.0,
            thrust=500,
            rotate_speed=2.0,
            energy=700,
        )
        bounds = Circle(
            radius=bullet_sprite.width / 2, color=Color.Red , num_segments=100,
            slide_x=(bullet_sprite.height/2 - bullet_sprite.width/2) * 0.8, slide_y=00)

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

        bullet.power = power

        return bullet