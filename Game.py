from util import *
from Level import *
from Tileset import *
from Prop import *

GAMES_DIRECTORY = 'games'

class Game(Saveable):
    '''
        This class represents a Game
    '''

    def __init__(self, title="New Game"):
        self.title = title
        self.ID = None
        self.directory = os.path.join(GAMES_DIRECTORY, self.title.strip().replace(' ', '_'))

    def initFiles(self):
        os.makedirs(self.getDir())

        # Save metadata
        self.save()

        # Create folders if they do not exist
        directories = [
            self.getLevelsDir(),
            self.getImgDir(),
            os.path.join(self.getImgDir(), 'characters'),
            os.path.join(self.getImgDir(), 'props'),
            os.path.join(self.getImgDir(), 'tiles'),
            self.getAudioDir(),
            os.path.join(self.getAudioDir(), 'music'),
            os.path.join(self.getAudioDir(), 'sfx'),
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

    def getAudioDir(self):
        return os.path.join(self.getDir(), 'audio')

    def getTileDir(self):
        return os.path.join(self.getImgDir(), "tiles")

    def getPropDir(self):
        return os.path.join(self.getImgDir(), "props")

    def setID(self, ID):
        if self.ID is not None:
            return

        self.ID = ID
        self.save()

    def setTitle(self, title):
        self.title = title
        self.save()

    def getAllTilesets(self):
        tilesetPaths = getAllImagesInDir(self.getTileDir())
        tilesets = []

        for path in tilesetPaths:
            tilesets.append(Tileset(path))

        return tilesets

    def addLevel(self, name):
        level = Level(name, self.getLevelsDir())
        
        if not dirExists(level.getDir()):
            level.initFiles()
            flash("New level created: " + name)
        else:
            flash("Could not create level, directory already exists")

    def deleteLevel(self, levelID):
        levels = self.getAllLevels()

        for i in xrange(len(levels)):
            if levels[i].ID == levelID:
                levels[i].delete()
                break

    def getAllLevels(self):
        levels = []

        for path in os.listdir(self.getLevelsDir()):
            level = Level(path, self.getLevelsDir())
            level.load()
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
            props.append(Prop(path))

        return props

class GamesList:
    '''
        Manages the list of games and ensures unique IDs
    '''
    currentID = 0
    gamesDirectories = [os.path.join(GAMES_DIRECTORY, x) for x in os.listdir(GAMES_DIRECTORY)]
    games = []

    @staticmethod
    def getID():
        result = GamesList.currentID
        GamesList.currentID += 1

        return result

    @staticmethod
    def load(directory):
        result = Game()
        result.directory = directory
        result.load()

        return result

    @staticmethod
    def init():
        for directory in GamesList.gamesDirectories:
            GamesList.addGame(GamesList.load(directory))

    @staticmethod
    def addGame(game):
        if game.ID is None:
            game.setID(GamesList.getID())
        else:
            if game.ID >= GamesList.currentID:
                GamesList.currentID = game.ID + 1
        GamesList.games.append(game)

    @staticmethod
    def getByID(gameID):
        # TODO: use a hash map to index games
        for i in xrange(len(GamesList.games)):
            game = GamesList.games[i]
            if game.ID == gameID:
                return game

        return None

    @staticmethod
    def removeGame(gameID):
        '''
            Removes a game from the list and deletes it
            Throws: IOError
        '''
        for i in xrange(len(GamesList.games)):
            game = GamesList.games[i]
            if game.ID == gameID:
                shutil.rmtree(game.getDir())
                del GamesList.games[i]
                flash("Deleted Game " + game.title)
                break

    @staticmethod
    def getAllGames():
        '''
            Returns a list of Games
        '''
        return GamesList.games

GamesList.init()