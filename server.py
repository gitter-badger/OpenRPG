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

TILESET_DIRECTORY = "img/tiles"
LEVELS_CONFIG_FILE = "levels/levels.json"

class Level():
    def __init__(self, ID, name, width, height, npcs=[], tilesets=[], tileImages=[]):
        self.ID = ID
        self.name = name
        self.width = int(width)
        self.height = int(height)
        self.npcs = npcs
        self.tilesets = tilesets
        self.tileImages = tileImages

def loadLevelData():
    filePath = LEVELS_CONFIG_FILE
    try:
        f = open(filePath)
        s = f.read().replace('\n', '')
        f.close()
        config = json.loads(s)
    except Exception as e:
        print e
        return None

    return config

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

def getAllLevels():
    levelData = loadLevelData()["levels"]
    if levelData is None:
        print "Error: Failed to load tileset config data"
        return []

    levels = []
    for i in xrange(len(levelData)):
        datum = levelData[i]
        name = datum["name"]
        width = datum["width"]
        height = datum["height"]
        npcs = datum["npcs"]
        tilesets = datum["tilesets"]
        tileImages = datum["tileImages"]
        levels.append(Level(i, name, width, height, npcs, tilesets, tileImages))


    return levels

@app.route("/")
def showHomepage():
    return send_from_directory(".", "index.html")

@app.route("/game.html")
def showGame():
    return send_from_directory(".", "game.html")

@app.route("/src/<path:path>")
def sendCode(path):
    return send_from_directory("src", path)

@app.route('/levels')
def showLevels():
    return render_template("levels.html",
        levels=getAllLevels())

@app.route('/tilesets/<fileName>/edit')
def editTileset(fileName):
    tilesets = getAllTilesets()
    for i in xrange(len(tilesets)):
        if tilesets[i].fileName == fileName:
            return render_template("tileset_editor.html",
                tilesetDirectory=TILESET_DIRECTORY,
                tileset=tilesets[i])

@app.route('/levels/<int:i>/edit')
def editLevel(i):
    levels = getAllLevels()

    # TODO: Load only required tilesets
    return render_template("level_editor.html",
        tilesetDirectory=TILESET_DIRECTORY,
        tilesets=getAllTilesets(),
        level=levels[i])

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