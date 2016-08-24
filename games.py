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
    def __init__(self, title="New Game"):
        self.title = title

def getAllGames():
    gamesDirectories = [x[0] for x in os.walk(GAMES_DIRECTORY)]
    games = []

    for directory in gamesDirectories:
    	games.append(Game())

    return games

# List all games
@GAMES_PATH_BLUEPRINT.route('/games')
def showAllGames():
    return render_template("games.html",
        games=getAllGames())

# Create a new game
@GAMES_PATH_BLUEPRINT.route('/games/new')
def createGame():
    flash("Created new game: ")
    return redirect(url_for('GAMES_PATH_BLUEPRINT.showAllGames'))

# Send a file from the games directory
@GAMES_PATH_BLUEPRINT.route('/games/<path:path>')
def sendGamesFile(path):
    return send_from_directory("games", path)