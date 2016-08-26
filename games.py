'''
	This file contains all code related to the games/ directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os

GAMES_PATH_BLUEPRINT = Blueprint('GAMES_PATH_BLUEPRINT', __name__, template_folder='templates')

GAMES_DIRECTORY = "games"
GAMES_CONFIG_FILE = "games/games.json"

class Game:
    '''
        This class represents a Game
        It handles all saving and loading of data about the game
    '''
    def __init__(self, title="New Game"):
        self.title = title

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
            f.write(json.dumps(self.__dict__))
            f.close()
        except IOError as e:
            print e

    def load(self):
        '''
            Load metadata from JSON
        '''
        directory = self.getDir()
        try:
            f = open(os.path.join(directory, 'data.json'), 'r')
            self.__dict__ = json.load(f)
            f.close()
        except IOError as e:
            print e

def getAllGames():
    '''
        Returns a list of Games
    '''
    gamesDirectories = [x for x in os.listdir(GAMES_DIRECTORY)]
    games = []

    for directory in gamesDirectories:
    	games.append(Game(directory))
        games[-1].load()

    return games

'''
    Views
'''

# List all games
@GAMES_PATH_BLUEPRINT.route('/games')
def showAllGames():
    return render_template("games.html",
        games=getAllGames())

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