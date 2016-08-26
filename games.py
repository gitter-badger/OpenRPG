'''
	This file contains all code related to the games/ directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os

GAMES_PATH_BLUEPRINT = Blueprint('GAMES_PATH_BLUEPRINT', __name__, template_folder='templates')

GAMES_DIRECTORY = "games"
GAMES_CONFIG_FILE = "games/games.json"

GamesList = None

class Game:
    '''
        This class represents a Game
        It handles all saving and loading of data about the game
    '''

    def __init__(self, title="New Game", ID=None):
        self.title = title
        self.ID = ID

    def getDir(self):
        return os.path.join(GAMES_DIRECTORY, self.title.strip().replace(' ', ''))

    def getImgDir(self):
        return os.path.join(self.getDir(), 'img')

    def getAudioDir(self):
        return os.path.join(self.getDir(), 'audio')

    def save(self):
        '''
            Save JSON metadata
        '''
        directory = self.getDir()
        try:
            f = open(os.path.join(directory, 'data.json'), 'w')
            f.write(json.dumps(self.__dict__, indent=3))
            f.close()
        except IOError as e:
            print e

    def setID(self, ID):
        if self.ID is not None:
            return

        self.ID = ID
        self.save()

    @staticmethod
    def load(directory):
        '''
            Load metadata from a directory
        '''
        try:
            f = open(os.path.join(directory, 'data.json'), 'r')
            game = Game()
            game.__dict__ = json.load(f)
            f.close()

            return game
        except IOError as e:
            print e

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
    def init():
        for directory in GamesList.gamesDirectories:
            GamesList.addGame(Game.load(directory))

    @staticmethod
    def addGame(game):
        if game.ID is None:
            game.setID(GamesList.getID())
        else:
            GamesList.currentID = max(game.ID, GamesList.currentID)
        GamesList.games.append(game)

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
    # Create the directory for the game
    os.makedirs(newGame.getDir())

    # Save metadata
    newGame.save()

    # Add the game to the list
    GamesList.addGame(newGame)

    # Create the directories for the game's images
    os.makedirs(newGame.getImgDir())
    os.makedirs(os.path.join(newGame.getImgDir(), 'characters'))
    os.makedirs(os.path.join(newGame.getImgDir(), 'floors'))
    os.makedirs(os.path.join(newGame.getImgDir(), 'props'))
    os.makedirs(os.path.join(newGame.getImgDir(), 'tiles'))

    # Create the directories for the game's audio
    os.makedirs(newGame.getAudioDir())
    os.makedirs(os.path.join(newGame.getAudioDir(), 'music'))
    os.makedirs(os.path.join(newGame.getAudioDir(), 'sfx'))


    flash("Created new game: " + gameTitle)
    return redirect(url_for('GAMES_PATH_BLUEPRINT.showAllGames'))

# Send a file from the games directory
@GAMES_PATH_BLUEPRINT.route('/games/<path:path>')
def sendGamesFile(path):
    return send_from_directory("games", path)