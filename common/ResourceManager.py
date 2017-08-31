import json, os
from enum import Enum
import platform
import random


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
        with open(self._db.get(name)) as json_data:
            data = json.load(json_data)
            return data

    def getProperty(self, name, key):
        with open(self._db.get(name)) as json_data:
            data = json.load(json_data)
            value = data.get(key)
            return value


class PropertyManager(object):
    def __init__(self, jsonManager, name):
        self._name = name
        self._manager = jsonManager
        self._db = None

    def update(self):
        self._db = self._manager.getDB(self._name)

    def _getDB(self):
        if self._db:
            return self._db
        self._db = self._manager.getDB(self._name)
        return self._db


