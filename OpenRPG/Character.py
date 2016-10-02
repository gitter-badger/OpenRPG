from util import *
from ComponentBin import ComponentBin

class Character(Saveable):
    @staticmethod
    def createCharacterComponentBin(parent):
        '''
            Creates a character component bin for a given parent
        '''
        return ComponentBin(parent)

    @staticmethod
    def getAllComponentBins(parent):
        path = parent.getCharacterComponentsDir()
        folders = os.listdir(path)
        bins = []

        for folder in folders:
            bins.append(ComponentBin.loadFromDir(parent, folder))

        bins.sort()
        return bins

    class Node():
        def __init__(self, component, offsetX, offsetY, rotation, scale):
            self.component = component
            self.x = offsetX
            self.y = offsetY
            self.theta = rotation
            self.scale = scale
            self.children = []

    def __init__(self, directory):
        self._directory = directory
        self.tree = Node(None, 0, 0, 0, 1)

    def getRoot(self):
        '''
            Returns the root node of this character's component tree
        '''
        return self.tree

    def randomizeComponents(self):
        '''
            Randomizes components by bin
        '''
        pass