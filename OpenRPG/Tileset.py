import os
from util import *

class Tileset(Saveable):
    @staticmethod
    def nameToDir(name):
        return name.replace(' ', '_')

    def __init__(self, name, parent):
        self.name = name
        self._parent = parent
        self.tileSize = 32
        self.xoff = 0
        self.yoff = 0
        self.imageID = getIdentifier()

        if os.path.exists(self.getSaveFilePath()):
            self.load()
        else:
            self.save()

    def getPath(self):
        return os.path.join(self.getDir(), self.name)

    def getURL(self):
        return os.path.sep + self.getPath() + '?cacheID=' + self.imageID

    def getDir(self):
        return self._parent.getTileDir()

    def getSaveFilePath(self):
        return os.path.join(self.getDir(), self.name.replace('.png', '_config.json'))