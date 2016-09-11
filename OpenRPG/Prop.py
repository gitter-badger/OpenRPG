from util import *

class Prop(Saveable):
    def __init__(self, path):
        self.name = path.split(os.sep)[-1]
        self.directory = os.sep.join(path.split(os.sep)[:-1])
        self.path = path

        if os.path.exists(self.getSaveFilePath()):
            self.load()
        else:
            self.save()

    def getSaveFilePath(self):
        return os.path.join(self.directory, self.name.replace('.png', '_config.json'))