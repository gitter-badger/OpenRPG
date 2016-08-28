'''
	This file contains all code related to the games/ directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os
import shutil
from level import Level
from util import *

GAMES_PATH_BLUEPRINT = Blueprint('GAMES_PATH_BLUEPRINT', __name__, template_folder='templates')

GAMES_DIRECTORY = 'games'

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

class Game(Saveable):
    '''
        This class represents a Game
        It handles all saving and loading of data about the game
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
            os.path.join(self.getImgDir(), 'floors'),
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

    def setID(self, ID):
        if self.ID is not None:
            return

        self.ID = ID
        self.save()

    def getAllTilesets(self):
        tilesets = []
        tileDir = self.getTileDir()

        for path in os.listdir(self.getTileDir()):
            if path.endswith(".png"):
                tilesets.append(Tileset(os.path.join(tileDir, path)))

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
            print level.directory
            level.load()
            levels.append(level)

        return levels

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

'''
    Views
'''

# List all games
@GAMES_PATH_BLUEPRINT.route('/games')
def showAllGames():
    return render_template("games.html",
        games=GamesList.getAllGames())

# Create a new game
@GAMES_PATH_BLUEPRINT.route('/games/new', methods=['POST'])
def createGame():
    gameTitle = request.form['gameTitle']
    newGame = Game(gameTitle)
    
    # Set up the directory structure for the game
    # If the folder exists already, exit with an error
    if os.path.isdir(newGame.getDir()):
        flash("Failed to create game. Directory already exists!")
        return redirect(url_for('GAMES_PATH_BLUEPRINT.showAllGames'))

    newGame.initFiles()
    GamesList.addGame(newGame)

    flash("Created new game: " + gameTitle)

    return redirect(url_for('GAMES_PATH_BLUEPRINT.showAllGames'))

# Delete a game
@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/delete', methods=['POST'])
def deleteGame(gameID):
    try:
        GamesList.removeGame(gameID)
    except IOError as e:
        print e
        flash("Something went wrong!")
    
    return redirect(url_for('GAMES_PATH_BLUEPRINT.showAllGames'))

# Edit a game
@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/edit')
def editGame(gameID):
    game = GamesList.getByID(gameID)

    return render_template("editGame.html",
        game=game,
        tilesets=game.getAllTilesets(),
        levels=game.getAllLevels())

# Send a file from the games directory
@GAMES_PATH_BLUEPRINT.route('/games/<path:path>')
def sendGamesFile(path):
    return send_from_directory("games", path)

# Create a tileset
@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/tilesets/add', methods=['POST'])
def addTileset(gameID):
    # TODO: Check if file exists
    # TODO: Make docstrings consistent: ''' '''
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
    elif not file.filename.endswith('.png'):
        flash('Upload failed: file type must be .png')
    else:
        directory = GamesList.getByID(gameID).getTileDir()
        destination = os.path.join(directory, file.filename)
        file.save(destination)

    return redirect(url_for('GAMES_PATH_BLUEPRINT.editGame',
        gameID=gameID))

# Edit a tileset
@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/tilesets/<string:name>/edit')
def editTileset(gameID, name):
    game = GamesList.getByID(gameID)
    tileset = None

    for t in game.getAllTilesets():
        if t.name == name:
            tileset = t
            break

    return render_template('editTileset.html',
        game=game,
        tileset=tileset)

# Update a tileset
@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/tilesets/<string:name>/update', methods=['POST'])
def updateTileset(gameID, name):
    game = GamesList.getByID(gameID)
    tileset = None

    for t in game.getAllTilesets():
        if t.name == name:
            tileset = t
            break

    # Write values and save
    tileset.tileSize = max(int(request.form['tileSize']), 1)
    tileset.xoff = int(request.form['xoff'])
    tileset.yoff = int(request.form['yoff'])
    tileset.save()

    return redirect(url_for('GAMES_PATH_BLUEPRINT.editTileset',
        gameID=gameID,
        name=name))

# Create a new level
@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/levels/new', methods=['POST'])
def createLevel(gameID):
    GamesList.getByID(gameID).addLevel(request.form['name'])

    return redirect(url_for('GAMES_PATH_BLUEPRINT.editGame',
        gameID=gameID))

# Delete a level
@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/levels/<int:levelID>/delete', methods=['POST'])
def deleteLevel(gameID, levelID):
    GamesList.getByID(gameID).deleteLevel(levelID)

    flash("Level deleted")

    return redirect(url_for('GAMES_PATH_BLUEPRINT.editGame',
        gameID=gameID))
