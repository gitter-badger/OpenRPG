'''
    This file contains code for the server
    It serves static files
    It also accepts new/updated files
'''

from os import listdir
import os.path
from flask import Flask, request, send_from_directory, render_template

app = Flask(__name__)

TILESET_DIRECTORY = "img/tiles"

class Tileset():
    def __init__(self, fileName, size=32, xoff=0, yoff=0):
        self.fileName = fileName
        self.size = size
        self.xoff = xoff
        self.yoff = yoff

def getAllTilesets():
    tilesets = []

    files = listdir(TILESET_DIRECTORY)
    for file in files:
        if file.endswith(".png"):
            tilesets.append(Tileset(file))

    return tilesets

@app.route("/")
def showHomepage():
    return send_from_directory(".", "index.html")

@app.route("/game.html")
def showGame():
    return send_from_directory(".", "game.html")

@app.route("/src/<path:path>")
def sendCode(path):
    return send_from_directory("src", path)

@app.route('/games/<path:path>')
def sendGamesFile(path):
    return send_from_directory("games", path)

@app.route('/'  + TILESET_DIRECTORY + '/<path:path>')
def sendTileset(path):
    return send_from_directory(TILESET_DIRECTORY, path)

@app.route('/tilesets')
def showTilesets():
    return render_template("tilesets.html",
        tilesets=getAllTilesets())

@app.route('/tilesets/<fileName>/edit')
def editTileset(fileName):
    tilesets = getAllTilesets()
    for i in xrange(len(tilesets)):
        if tilesets[i].fileName == fileName:
            return render_template("tileset_editor.html",
                tilesetDirectory=TILESET_DIRECTORY,
                tileset=tilesets[i])

if __name__ == '__main__':
    app.run(debug=True)