from util import *

class Tileset(Saveable):
    def __init__(self, path):
        self.name = path.split(os.sep)[-1]
        self.directory = os.sep.join(path.split(os.sep)[:-1])
        self.path = path
        self.tileSize = 32
        self.xoff = 0
        self.yoff = 0

        if os.path.exists(self.getSaveFilePath()):
            self.load()
        else:
            self.save()

    def getSaveFilePath(self):
        return os.path.join(self.directory, self.name.replace('.png', '_config.json'))