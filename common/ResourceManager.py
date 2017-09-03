import json, os
from enum import Enum
import platform
import random

class SpriteParameter(Enum):
    FILENAME = "file"
    FILESNAME = "files"
    SCALE = "scale"
    ROTATION = "rotation"
    TYPE_IMAGE = "typeImage"
    TYPE = "type"
    DURATION = "duration"
    LOOPED = "looped"

class ObjectParameter(Enum):
    THRUST = "thrust"
    RESISTANCE = "resistance"
    ROTATE_SPEED = "rotateSpeed"
    MAGAZINE = "magazine"
    LIVE = "live"
    COST_BULLET = "costBullet"
    RECOVERY_MAGAZINE = "recoveryMagazine"
    RECOVERY_ENERGY = "recoveryEnergy"
    CONSUMPTION_ENERGY = "consumptionEnergy"
    POWER_BANK = "powerBank"
    RESET_ENGINE = "resetEngine"
    WEAPON_POWER = "weaponPower"
    CONST_RELOAD_WEAPON_TIME = "constReloadWeaponTime"
    CONST_RECOVERY_ENGINE_TIME = "constRecoveryEngineTime"
    CONST_RESET_ENGINE_TIME = "constResetEngineTime"
    CONST_ROTATE_FACTOR = "constRotateFactor"
    CONST_ROTATE_STEP_FACTOR = "constRotateStepFactor"
    DAMAGE = "damage"
    ENERGY = "energy"
    WEAPON = "weapon"
    COUNT_SPLINTERS = "countSplinters"
    BONUS = "bonus"
    MAX_SPEED = "maxSpeed"
    FIRING_SPEED = "firingSpeed"

class JsonManager(object):
    def __init__(self, work_dir="."):
        self._db = {}
        self._work_dir = os.path.abspath(os.path.dirname(work_dir))
        self._data = None
        print(self._work_dir)

    def addJsonData(self, name,  file):
        try:
            self._db.update({name: "%s\\%s" % (self._work_dir, file)})
        except IOError as ex:
            print("ReadJson: {}".format(ex))

    def getDB(self, name):
        try:
            with open(self._db.get(name)) as json_data:
                data = json.load(json_data)
                return data
        except Exception as ex:
            print("Expect this jsonBase {}".format(name))
            return None

    def getProperty(self, name, key):
        with open(self._db.get(name)) as json_data:
            data = json.load(json_data)
            value = data.get(key)
            return value


class PropertyManager(object):
    def __init__(self, jsonManager):
        self._manager = jsonManager

    def _getDB(self, name):
        return self._manager.getDB(name)

    def get_sprite(self, name_object, parameter):
        try:
            value = self._getDB(name_object).get("sprite").get(parameter.value)
        except AttributeError as ex:
            return None
        else:
            return value


    def get_parameter(self, name_object, parameter):
        try:
            value = self._getDB(name_object).get("parameters").get(parameter.value)
        except AttributeError as ex:
            return None
        else:
            return value

