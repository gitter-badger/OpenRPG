import os
from util import *

class Prop(Saveable):
    def __init__(self, name, parent):
        self.name = name
        self._parent = parent

        if os.path.exists(self.getSaveFilePath()):
            self.load()
        else:
            self.save()

    def getDir(self):
        return self._parent.getPropDir()

    def getPath(self):
        return os.path.join(self.getDir(), self.name)

    def getSaveFilePath(self):
        return os.path.join(self.getDir(), self.name.replace('.png', '_config.json'))