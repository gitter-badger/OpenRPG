import os
from util import *
from Component import Component

class ImageComponent(Component):
    def __init__(self, parent, imagePath=None, originX=0, originY=0):
        self._parent = parent

        if imagePath is not None:
            self.load()
        else:
            self.name = 'New Image Component ' + str(ImageComponent.nextID())
            self.originX = originX
            self.originY = originY
            self.imageURL = '' # TODO
            self.cacheID = getIdentifier()
            self.save()

    def getDir(self):
        return os.path.join(self._parent.getDir(), nameToDir(self.name))

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

