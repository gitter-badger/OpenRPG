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

    def __init__(self, name, directory):
        self.name = name
        self.setDirectory(directory)
        if not dirExists(self.directory):
            self.width = 640
            self.height = 480
            self.ID = Level.getID()
            os.makedirs(self.directory)
            self.createEmptyFloorplan()
            self.save()
        else:
            self.load()

    def createEmptyFloorplan(self):
        png.from_array([[0, 0, 0, 0]], 'RGBA').save(self.getFloorplanPath())

    def setDirectory(self, directory):
        self.directory = os.path.join(directory, Level.nameToDir(self.name))

    def load(self):
        super(self.__class__, self).load()

        if self.ID > Level.currentID:
            Level.currentID = self.ID

    def delete(self):
        shutil.rmtree(self.getDir())
        
    def getDir(self):
        return self.directory

    def getFloorplanPath(self):
        return os.path.join(self.getDir(), 'floorplan.png')

    @staticmethod
    def getID():
        Level.currentID += 1
        return Level.currentID