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
        '''
            Converts a game title into a directory name
        '''
        return os.path.join(Game.GAMES_DIRECTORY, name.strip().replace(' ', '_'))

    @staticmethod
    def loadFromDirectory(directory):
        '''
            Loads game data from a directory path
            Returns a new Game
        '''
        result = Game('', False)
        result.directory = directory
        result.load()

        return result

    def __init__(self, title='New Game', createFiles=True):
        self.title = title
        self.ID = None
        self.directory = Game.dirFromName(self.title)
        if createFiles:
            self.initFiles()

    def setTitle(self, title):
        '''
            Sets the title of the game
        '''
        self.title = title
        oldDirectory = self.directory
        self.directory = Game.dirFromName(self.title)
        os.rename(oldDirectory, self.directory)
        self.save()

    def initFiles(self):
        '''
            Initializes the files and directories of the game
        '''
        if not dirExists(self.getDir()):
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
            self.getSfxDir(),
            self.getCharacterComponentsDir()
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
        return os.path.join(self.getDir(), 'characters')

    def getCharacterComponentsDir(self):
        return os.path.join(self.getCharactersDir(), 'components')

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
        '''
            Sets the ID of the game
            If the ID is already set: does nothing
        '''
        if self.ID is not None:
            return

        self.ID = ID
        self.save()

    def getAllTilesets(self):
        '''
            Returns a list of Tilesets belonging to this game
        '''
        tilesetPaths = getAllImagesInDir(self.getTileDir())
        tilesets = []

        for path in tilesetPaths:
            name = path.split(os.sep)[-1]
            tilesets.append(Tileset(name, self))

        return tilesets

    def addLevel(self, name):
        '''
            Adds a new level to the game
        '''
        if dirExists(os.path.join(self.getLevelsDir(), nameToDir(name))):
            return None

        return Level(name, self)

    def deleteLevel(self, levelID):
        '''
            Deletes a level by ID
        '''
        levels = self.getAllLevels()

        for i in xrange(len(levels)):
            if levels[i].ID == levelID:
                levels[i].delete()
                break

    def getAllLevels(self):
        '''
            Returns a list of Levels in this game
        '''
        levels = []

        for path in os.listdir(self.getLevelsDir()):
            level = Level(path, self)
            levels.append(level)

        return levels

    def getLevelByID(self, levelID):
        '''
            Returns a Level from this game by ID
        '''
        for level in self.getAllLevels():
            if level.ID == levelID:
                return level

        flash("Error: No such level")

    def getAllProps(self):
        '''
            Returns a list of all Props for this game
        '''
        propPaths = getAllImagesInDir(self.getPropDir())
        props = []

        for path in propPaths:
            props.append(Prop(path.split(os.sep)[-1], self))

        return props

    def delete(self):
        '''
            Deletes the files and folders for this game
        '''
        shutil.rmtree(self.getDir())

