from flask import flash
from util import *
from Level import *
from Tileset import *
from Prop import *

class Game(Saveable):
    '''
        This class represents a Game
    '''
    GAMES_DIRECTORY = 'games'

    @staticmethod
    def dirFromName(name):
        return os.path.join(Game.GAMES_DIRECTORY, name.strip().replace(' ', '_'))

    def __init__(self, title='New Game'):
        self.title = title
        self.ID = None
        self.directory = Game.dirFromName(self.title)

    def setTitle(self, title):
        self.title = title
        oldDirectory = self.directory
        self.directory = Game.dirFromName(self.title)
        os.rename(oldDirectory, self.directory)
        self.save()

    def initFiles(self):
        os.makedirs(self.getDir())

        # Save metadata
        self.save()

        # Create folders if they do not exist
        directories = [
            self.getLevelsDir(),
            self.getImgDir(),
            self.getCharactersDir(),
            self.getPropsDir(),
            self.getTileDir(),
            self.getAudioDir(),
            self.getMusicDir(),
            self.getSfxDir()
        ]

        for directory in directories:
            if not dirExists(directory):
                os.makedirs(directory)
        
    def getDir(self):
        return self.directory

    def getLevelsDir(self):
        return os.path.join(self.getDir(), 'levels')

    def getImgDir(self):
        return os.path.join(self.getDir(), 'img')

    def getCharactersDir(self):
        return os.path.join(self.getImgDir(), 'characters')

    def getPropsDir(self):
        return os.path.join(self.getImgDir(), 'props')

    def getTileDir(self):
        return os.path.join(self.getImgDir(), 'tiles')

    def getPropDir(self):
        return os.path.join(self.getImgDir(), 'props')

    def getAudioDir(self):
        return os.path.join(self.getDir(), 'audio')

    def getMusicDir(self):
        return os.path.join(self.getAudioDir(), 'music')

    def getSfxDir(self):
        return os.path.join(self.getAudioDir(), 'sfx')

    def setID(self, ID):
        if self.ID is not None:
            return

        self.ID = ID
        self.save()

    def getAllTilesets(self):
        tilesetPaths = getAllImagesInDir(self.getTileDir())
        tilesets = []

        for path in tilesetPaths:
            name = path.split(os.sep)[-1]
            tilesets.append(Tileset(name, self))

        return tilesets

    def addLevel(self, name):
        if dirExists(os.path.join(self.getLevelsDir(), Level.nameToDir(name))):
            flash("Could not create level, directory already exists")
            return

        level = Level(name, self)
        flash("New level created: " + name)

    def deleteLevel(self, levelID):
        levels = self.getAllLevels()

        for i in xrange(len(levels)):
            if levels[i].ID == levelID:
                levels[i].delete()
                break

    def getAllLevels(self):
        levels = []

        for path in os.listdir(self.getLevelsDir()):
            level = Level(path, self)
            levels.append(level)

        return levels

    def getLevelByID(self, levelID):
        for level in self.getAllLevels():
            if level.ID == levelID:
                return level

        flash("Error: No such level")

    def getAllProps(self):
        propPaths = getAllImagesInDir(self.getPropDir())
        props = []

        for path in propPaths:
            props.append(Prop(path.split(os.sep)[-1], self))

        return props

    def delete(self):
        shutil.rmtree(self.getDir())

