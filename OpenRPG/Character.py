from util import *

class Character(Saveable):
    class Node():
        def __init__(self, component, offsetX, offsetY, rotation, scale):
            self.component = component
            self.x = offsetX
            self.x = offsetY
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