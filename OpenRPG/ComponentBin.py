import os
from util import *

class ComponentBin(Saveable):
    currentID = 0

    @staticmethod
    def getID():
        result = ComponentBin.currentID
        ComponentBin.currentID += 1

        return result

    @staticmethod
    def loadFromDir(parent, folder):
        '''
            Loads a ComponentBin from a directory
        '''

        return ComponentBin(parent, folder)

    def __init__(self, parent, name=None):
        self._parent = parent

        if name is None:
            self.ID = ComponentBin.getID()
            self.name = 'New Bin ' + str(self.ID)
            self.components = []

            os.mkdir(self.getDir())
            self.save()
        else:
            self.name = name
            self.load()
            ComponentBin.currentID = max(ComponentBin.currentID, self.ID + 1)

    def __lt__(self, other):
        return self.name < other.name

    def getDir(self):
        return os.path.join(self._parent.getCharacterComponentsDir(), nameToDir(self.name))