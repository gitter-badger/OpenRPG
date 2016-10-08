import os
from util import *
from Component import Component

class ImageComponent(Component):
    def __init__(self, parent, directory=None, originX=0, originY=0):
        self._parent = parent
        self.directory = directory

        if directory is not None:
            self.load()
        else:
            self.ID = ImageComponent.nextID()
            self.name = 'New Image Component ' + str(self.ID)
            self.directory = nameToDir(self.name)
            self.originX = originX
            self.originY = originY
            self.imageURL = '' # TODO
            self.cacheID = getIdentifier()
            self.save()

    def __lt__(self, other):
        return self.ID < other.ID

    def getDir(self):
        return os.path.join(self._parent.getDir(), self.directory)

    def getURL(self):
        '''
            Returns a URL to this component's image
        '''
        return self.imageURL + '?cacheID=' + str(self.cacheID)

    def getCode(self):
        '''
            Returns code for rendering this component
        '''
        pass

