'''
    
'''

import json
import os
import shutil
from util import *

class Level(Saveable, object):
    currentID = -1

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
            self.createBlankImages()
            self.save()
        else:
            self.load()

    def __lt__(self, other):
        return self.name < other.name

    def updateFloorplanImageID(self):
        '''
            Changes the floorplan ID so the browser will update its cache
        '''
        self._floorplanImageID = getIdentifier()
        self.save()

    def createBlankImages(self):
        '''
            Creates placeholder images
        '''
        createEmptyImage(self.getFloorplanPath())
        createEmptyImage(self.getBackgroundPath())

    def getDir(self):
        '''
            Returns the path to this Level's directory
        '''
        return os.path.join(self._parent.getLevelsDir(), nameToDir(self.name))

    def load(self):
        '''
            Overrides Saveable.load
            Loads the level from the directory
        '''
        super(self.__class__, self).load()

        if self.ID > Level.currentID:
            Level.currentID = self.ID

    def delete(self):
        '''
            Deletes the directory and files associated with this Level
        '''
        shutil.rmtree(self.getDir())

    def getFloorplanPath(self):
        '''
            Returns the file path on the server to this Level's floorplan image
        '''
        return os.path.join(self.getDir(), 'floorplan.png')
        
    def getFloorplanURL(self):
        '''
            Returns a URL to this Level's floorplan image
        '''
        return os.path.sep + os.path.join(self.getDir(), 'floorplan.png?cacheID=' + self._floorplanImageID)

    def getBackgroundPath(self):
        '''
            Returns the file path on the server to this Level's background image
        '''
        return os.path.join(self.getDir(), 'background.png')

    def getBackgroundURL(self):
        '''
            Returns a URL to this Level's background image
        '''
        return os.path.sep + self.getBackgroundPath()

    @staticmethod
    def getID():
        Level.currentID += 1
        return Level.currentID