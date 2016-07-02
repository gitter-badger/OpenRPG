'''
    This file contains code for the server
    It serves static files
    It also accepts new/updated files
'''

from os import listdir
import os.path
from flask import Flask, request, send_from_directory, render_template, url_for, redirect
import json

app = Flask(__name__)

TILESET_DIRECTORY = "img/tiles"

class Tileset():
    def __init__(self, fileName, size=32, xoff=0, yoff=0):
        self.fileName = fileName
        self.size = size
        self.xoff = xoff
        self.yoff = yoff

def loadTilesetConfigData():
    filePath = TILESET_DIRECTORY + "/" + "config.json"
    try:
        f = open(filePath)
        s = f.read().replace('\n', '')
        f.close()
        config = json.loads(s)
    except Exception as e:
        print e
        return None

    return config

def writeTilesetConfigData(config):
    filePath = TILESET_DIRECTORY + "/" + "config.json"
    try:
        f = open(filePath, 'w')
        f.write(json.dumps(config, sort_keys=True, indent=3))
        f.close()
    except Exception as e:
        print e

def getAllTilesets():
    config = loadTilesetConfigData()
    if config is None:
        print "Error: Failed to load tileset config data"
        config = dict()

    tilesets = []

    files = listdir(TILESET_DIRECTORY)
    for file in files:
        if file.endswith(".png"):
            if not file in config:
                config[file] = dict()
                config[file]["size"] = 32
                config[file]["xoff"] = 0
                config[file]["yoff"] = 0
            size = config[file]["size"]
            xoff = config[file]["xoff"]
            yoff = config[file]["yoff"]

            tilesets.append(Tileset(file, size, xoff, yoff))

    # Save config data
    writeTilesetConfigData(config)

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

@app.route('/tilesets/<fileName>/update', methods=['POST'])
def updateTileset(fileName):
    config = loadTilesetConfigData()
    if config is None:
        print "Error: Failed to load tileset config data"
    if not fileName in config:
        config[fileName] = dict()


    config[fileName]["size"] = request.form["size"]
    config[fileName]["xoff"] = request.form["xoff"]
    config[fileName]["yoff"] = request.form["yoff"]

    writeTilesetConfigData(config)
    
    dest = '/tilesets/' + fileName + '/edit'
    print dest
    return redirect(url_for("editTileset", fileName=fileName))

if __name__ == '__main__':
    app.run(debug=True)