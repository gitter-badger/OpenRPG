import os
from util import *
from ImageComponent import *

class ComponentBin(Saveable):
    @staticmethod
    def loadFromDir(parent, folder):
        '''
            Loads a ComponentBin from a directory
        '''

        return ComponentBin(parent, folder)

    def __init__(self, parent, directory=None):
        self._parent = parent
        self.directory = directory

        if directory is None:
            self.ID = ComponentBin.nextID()
            self.name = 'New Bin ' + str(self.ID)
            self.directory = nameToDir(self.name)

            os.mkdir(self.getDir())
            self.save()
        else:
            self.load()
            ComponentBin.currentID = max(ComponentBin.currentID, self.ID + 1)

    def __lt__(self, other):
        return self.ID < other.ID

    def getDir(self):
        return os.path.join(self._parent.getComponentsDir(), self.directory)

    def createComponent(self):
        '''
            Creates a new empty ImageComponent in this bin
            Returns the new ImageComponent
        '''
        return ImageComponent(self)

    def getAllComponents(self):
        '''
            Returns all the components in this bin
        '''
        components = []

        for directory in listdirs(self.getDir()):
            components.append(ImageComponent(self, directory))

        components.sort()

        return components