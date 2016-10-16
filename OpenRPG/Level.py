import json
import os
import shutil
from util import *

class Level(Saveable, object):
    '''
        This class represents one level within a game.
    '''

    def __init__(self, name, parent):
        self.name = name
        self._floorplanImageID = getIdentifier()
        self._parent = parent

        if self.name is None:
            self.width = 640
            self.height = 480
            self.ID = Level.nextID()
            self.name = 'New Level ' + str(self.ID)
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

    def getWorldObjectJSON(self):
        '''
            Returns a JSON string describing the World object for this Level
        '''
        world = GameObject('World')

        return json.dumps(word)