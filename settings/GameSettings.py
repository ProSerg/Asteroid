import pyglet
import os

from Asteroid.common.ResourceManager import *

class GameSettings(object):
    work_dir = os.path.realpath("%s\\..\\" % os.path.dirname(os.path.realpath(__file__)))
    _DB_SETTINGS_ = "settings"

    def __init__(self):
        self.jsonManager = JsonManager(work_dir=os.path.realpath("%s\\resources\\" % self.work_dir))
        self.jsonManager.addJsonData(self._DB_SETTINGS_, "gameSettings.json")


    def pyGletSetup(self):
        for lib in self.getParameter(SettingsParameter.LOADLIBS):
            pyglet.lib.load_library(os.path.realpath("{dir}\\{lib}".format(
                dir="%s\\dependences" % self.work_dir,
                lib=lib)))

        pyglet.have_avbin = True
        pyglet.options['audio'] = ('openal', 'silent')

    def getParameter(self, parameter):
        return self.jsonManager.getProperty(self._DB_SETTINGS_, parameter.value)






