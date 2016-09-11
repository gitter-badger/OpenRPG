'''
    This file contains code for the server
    It serves static files
    It also accepts new/updated files
'''

from os import listdir
import os.path
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash
from games import *
import random, string

app = Flask(__name__)
app.secret_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64))
app.register_blueprint(GAMES_PATH_BLUEPRINT)

@app.route("/")
def showHomepage():
    return render_template("index.html")

@app.route("/static/<path:path>")
def sendFromStatic(path):
    return send_from_directory(".", path)

@app.route("/game.html")
def showGame():
    return send_from_directory(".", "game.html")

@app.route("/src/<path:path>")
def sendCode(path):
    return send_from_directory("src", path)

@app.route("/img/<path:path>")
def sendImage(path):
    return send_from_directory("img", path)

@app.route("/games/<path:path>")
def sendFromGames(path):
    return send_from_directory("games", path)

if __name__ == '__main__':
    app.run(debug=True)