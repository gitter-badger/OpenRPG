'''
    
'''

import json
import os
import shutil
import png
from util import *

class Level(Saveable, object):
    currentID = -1

    @staticmethod
    def nameToDir(name):
        return name.replace(' ', '_')

    @staticmethod
    def getUniqueLevelName():
        return 'New Level ' + str(Level.currentID + 1)

    def __init__(self, name, parent):
        self.name = name
        self._floorplanImageID = getIdentifier()
        self._parent = parent

        if not dirExists(self.getDir()):
            self.width = 640
            self.height = 480
            self.ID = Level.getID()
            os.makedirs(self.getDir())
            self.createEmptyFloorplan()
            self.save()
        else:
            self.load()

    def updateFloorplanImageID(self):
        self._floorplanImageID = getIdentifier()
        self.save()

    def createEmptyFloorplan(self):
        png.from_array([[0, 0, 0, 0]], 'RGBA').save(self.getFloorplanPath())

    def getDir(self):
        return os.path.join(self._parent.getLevelsDir(), Level.nameToDir(self.name))

    def load(self):
        super(self.__class__, self).load()

        if self.ID > Level.currentID:
            Level.currentID = self.ID

    def delete(self):
        shutil.rmtree(self.getDir())

    def getFloorplanPath(self):
        return os.path.join(self.getDir(), 'floorplan.png')
        
    def getFloorplanURL(self):
        return os.path.sep + os.path.join(self.getDir(), 'floorplan.png?cacheID=' + self._floorplanImageID)

    @staticmethod
    def getID():
        Level.currentID += 1
        return Level.currentID