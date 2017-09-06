from Asteroid.Items.ItemObject import ItemObject
from Asteroid.UserUI import UserUI
from Asteroid.common.Figure import *
from Asteroid.common.Mechanics import *
from Asteroid.common.Collisions import *
from Asteroid.common.UnitManager import *
from Asteroid.common.AnimationManager import *
from Asteroid.common.ResourceManager import *

import random
from pathlib import Path
# Set up a window

class TypeAsteroid(Enum):
    BIG = "big"
    MEDIUM = "medium"
    SMALL = "small"


class TypeItem(Enum):
    USERSHIP = "userShip"
    ASTEROID = "asteroid"
    BONUS = "bonus"
    BULLET = "bullet"
    EFFECTS = "effect"

class TypeShip(Enum):
    BUG = "bug"
    FIGHTER = "fighter"
    SAUCER = "saucer"

class GameMaster(object):
    NUMS_ASTEROIDS = 10

    def __init__(self, loader, batch):
        self._loader = loader
        self.batch = batch
        self.type_user_ship = TypeShip.SAUCER

        self.jsonManager = JsonManager()
        self.jsonManager.addJsonData("fighter", "resources\\fighterProperty.json")
        self.jsonManager.addJsonData("bug", "resources\\bugProperty.json")
        self.jsonManager.addJsonData("saucer", "resources\\saucerProperty.json")
        self.jsonManager.addJsonData("smallAsteroid",  "resources\\smallAsteroidProperty.json")
        self.jsonManager.addJsonData("mediumAsteroid", "resources\\mediumAsteroidProperty.json")
        self.jsonManager.addJsonData("bigAsteroid",    "resources\\bigAsteroidProperty.json")
        self.jsonManager.addJsonData("aBullet",        "resources\\aBullet.json")
        self.jsonManager.addJsonData("sBullet",        "resources\\sBullet.json")
        self.jsonManager.addJsonData("wBullet",        "resources\\wBullet.json")
        self.jsonManager.addJsonData("smallStar", "resources\\smallStarProperty.json")
        self.jsonManager.addJsonData("mediumStar", "resources\\mediumStarProperty.json")
        self.jsonManager.addJsonData("bigStar", "resources\\bigStarProperty.json")

        self.propertyManager = PropertyManager(self.jsonManager)

        self.unit_manager = UnitManager(self._loader, self.batch)
        self.anim_manager = AnimationManager(self._loader, self.batch)
        self.user_ui = UserUI(unit_manager=self.unit_manager, property_manager=self.propertyManager,
                              group=self._loader.ui, ship=self.type_user_ship.value, batch=self.batch)

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

        star_boom = [
            "galaxy_15.png",
            "galaxy_16.png",
            "explosion_0.png",
            "explosion_1.png",
            "explosion_2.png",
            "explosion_3.png",
            "explosion_4.png",
            "explosion_5.png",
            "explosion_6.png",
            "explosion_7.png",
            "explosion_8.png",
            "explosion_9.png",
            "explosion_10.png",
            "explosion_11.png",
            "explosion_12.png",
            "explosion_13.png",
            "explosion_14.png",
            "explosion_15.png",
        ]

        self.anim_manager.createSpringEffect(
            name="star_boom",
            img=star_boom,
            scale=.2, type_image="frames", duration=0.02, rotation=0, looped=False,
                                        anchor_x=0, anchor_y=0)

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

    def createAnimation(self, name, x, y,  rotation=0, group=None):
        return self.anim_manager.createAnimation(name, x, y, rotation, group=group)

    def createBackGround(self):
        x = 400
        y = 400
        fon1 = self.unit_manager.get_sprite(
            name="background_4.png",
            x=400,
            y=200,
            scale=1.0,
            rotation=0.0,
            group=self._loader.background,
        )
        fon2 = self.unit_manager.get_sprite(
            name="background_4.png",
            x=400,
            y=400,
            scale=1.0,
            rotation=0.0,
            group=self._loader.background,
        )
        return [fon1, fon2]

    def generate_asteroid(self, name,  x, y):
        rotation = random.randint(0, 360)
        asteroid = self.make_asteroid(
            name,  x, y, rotation,
            type_asteroid=random.choice([TypeAsteroid.BIG, TypeAsteroid.MEDIUM, TypeAsteroid.SMALL]))
        asteroid.mechanic.rotate_speed = random.randint(-200, 200)
        asteroid.mechanic.thrust = random.randint(50, 300)
        return asteroid

    def generate_splinters(self, parent):
        splinters = []
        for idx in range(0, parent.mechanic.countSplinters):
            splinter = self.make_asteroid(
                name="Asteroid",
                x=parent.sprite.x,
                y=parent.sprite.y,
                rotation=random.randint(0, 360),
                type_asteroid=TypeAsteroid.SMALL)
            splinter.mechanic.rotate_speed = parent.mechanic.rotate_speed - int(parent.mechanic.rotate_speed * 0.1)
            splinter.mechanic.thrust = parent.mechanic.thrust - int(parent.mechanic.thrust * 0.1)
            splinters.append(splinter)
        return splinters

    def make_asteroid(self, name,  x, y, rotation, type_asteroid):
        root = "{}Asteroid".format(type_asteroid.value)
        image = lambda images: random.choice(images) if type(images) is list else images
        asteroid_sprite = self.unit_manager.get_sprite(
                name=image(self.propertyManager.get_sprite(root, SpriteParameter.FILENAME)),
                scale=self.propertyManager.get_sprite(root, SpriteParameter.SCALE),
                rotation=rotation,
                group=self._loader.asteroids_group,
        )

        asteroid_mechanics = AsteroidMechanics(
            name=root,
            property_manager=self.propertyManager,
            type_asteroid=type_asteroid,
        )

        asteroid = ItemObject(
            x=x,
            y=y,
            name=name,
            type_item=TypeItem.ASTEROID,
            sprite=asteroid_sprite,
            rotation=rotation,
            mechanic=asteroid_mechanics,
            bounds=Rectangle(width=asteroid_sprite.width, height=asteroid_sprite.height, rotation=0, color=Color.Blue),
        )

        return asteroid

    def make_user_ship(self, x, y):
        root = self.type_user_ship.value

        sprite = self.unit_manager.get_sprite(
            name=self.propertyManager.get_sprite(root, SpriteParameter.FILENAME),
            scale=self.propertyManager.get_sprite(root, SpriteParameter.SCALE),
            rotation=self.propertyManager.get_sprite(root, SpriteParameter.ROTATION),
            group=self._loader.ship_group,
        )

        ship_mechanics = None

        if self.type_user_ship == TypeShip.FIGHTER:
            ship_mechanics = FighterMechanics(
                property_manager=self.propertyManager,
                callbackShoot=self.make_bullet
            )
        elif self.type_user_ship == TypeShip.BUG:
            ship_mechanics = BugMechanics(
                property_manager=self.propertyManager,
                callbackShoot=self.make_bullet
            )
        elif self.type_user_ship == TypeShip.SAUCER:
            ship_mechanics = SaucerMechanics(
                property_manager=self.propertyManager,
                callbackShoot=self.make_bullet
            )

        ship = ItemObject(
            x=x,
            y=y,
            name="UserShip",
            type_item=TypeItem.USERSHIP,
            sprite=sprite,
            rotation=self.propertyManager.get_sprite(root, SpriteParameter.ROTATION),
            mechanic=ship_mechanics,
            bounds=Rectangle(width=sprite.width, height=sprite.height, rotation=0, color=Color.Green),
        )

        if self.type_user_ship == TypeShip.FIGHTER:

            fire_image = [
                "fire_3.png",
                "fire_4.png",
                "fire_6.png",
                "fire_7.png",
                "fire_8.png",
            ]

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

    def make_star(self, x, y, type):
        root = "{}Star".format(type.value)

        star_sprite = self.anim_manager.getSpringEffect(
            img=self.propertyManager.get_sprite(root, SpriteParameter.FILENAME),
            type_image=self.propertyManager.get_sprite(root, SpriteParameter.TYPE_IMAGE),
            group=self._loader.foreground,
            scale=self.propertyManager.get_sprite(root, SpriteParameter.SCALE),
            looped=self.propertyManager.get_sprite(root, SpriteParameter.LOOPED),
            duration=self.propertyManager.get_sprite(root, SpriteParameter.DURATION),
            rotation=self.propertyManager.get_sprite(root, SpriteParameter.ROTATION))

        star_mechanics = StarMechanics(
            self.propertyManager.get_parameter(root, ObjectParameter.BONUS),
            self.propertyManager.get_parameter(root, ObjectParameter.LIVE)
        )

        star = ItemObject(
            x=x - star_sprite.width/2,
            y=y - star_sprite.height/2,
            name="Star",
            sprite=star_sprite,
            type_item=TypeItem.BONUS,
            rotation=0,
            mechanic=star_mechanics,
            bounds=Rectangle(width=star_sprite.width, height=star_sprite.height, rotation=0, color=Color.Green),
        )

        return star

    def make_bullet(self, x, y, rotation, weapon):
        bullet_sprite = self.unit_manager.get_sprite(
            name=self.propertyManager.get_sprite(weapon, SpriteParameter.FILENAME),
            scale=self.propertyManager.get_sprite(weapon, SpriteParameter.SCALE),
            rotation=self.propertyManager.get_sprite(weapon, SpriteParameter.ROTATION),
            group=self._loader.effects,
        )

        bullet_mechanics = BulletMechanics(
            property_manager=self.propertyManager,
            weapon=weapon)

        bounds = Circle(
            radius=bullet_sprite.width / 2, color=Color.Red , num_segments=100,
            slide_x=(bullet_sprite.height/2 - bullet_sprite.width/2) * 0.8, slide_y=00)

        bullet = ItemObject(
            x=x,
            y=y,
            local_x=15,
            local_y=0,
            name="bullet",
            type_item=TypeItem.BULLET,
            sprite=bullet_sprite,
            rotation=rotation,
            mechanic=bullet_mechanics,
            bounds=bounds,
        )
        return bullet