'''
    This file contains code for the server
'''

from os import listdir
import os.path
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash
from gameServer import *
from levelServer import *
from characterServer import *
from assetsServer import *
import random, string
from GamesList import GamesList

TEMPLATE_FOLDER = '../templates'
STATIC_FOLDER = '../static'

# App setup
app = Flask(__name__,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATIC_FOLDER)
app.secret_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64))
app.register_blueprint(GAMES_PATH_BLUEPRINT)
app.register_blueprint(LEVELS_PATH_BLUEPRINT)
app.register_blueprint(CHARACTERS_PATH_BLUEPRINT)

@app.route("/")
def showHomepage():
    return render_template("index.html",
        games=GamesList.getAllGames())

@app.route("/game.html")
def showGame():
    return render_template("game.html")

@app.route("/src/<path:path>")
def sendCode(path):
    return send_from_directory("../src", path)

@app.route("/games/<path:path>")
def sendFromGames(path):
    return send_from_directory("../games", path)

if __name__ == '__main__':
    app.run(debug=True)