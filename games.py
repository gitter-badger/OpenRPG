'''
	This file contains all code related to the games/ directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os
import shutil
from Level import Level
from Game import *
from util import *

GAMES_PATH_BLUEPRINT = Blueprint('GAMES_PATH_BLUEPRINT', __name__, template_folder='templates')

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

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/setTitle', methods=['POST'])
def setGameTitle(gameID):
    '''
        Sets a game's title
    '''
    game = GamesList.getByID(gameID)
    game.setTitle(request.form['gameTitle'])

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

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/levels/<int:levelID>/floorplan/edit')
def editLevelFloorplan(gameID, levelID):
    '''
        Edit the floorplan of a level
    '''
    game = GamesList.getByID(gameID)
    level = game.getLevelByID(levelID)

    return render_template('editLevelFloorplan.html',
        game=game,
        level=level,
        tilesets=game.getAllTilesets())

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/levels/<int:levelID>/floorplan/save', methods=['POST'])
def saveLevelFloorplan(gameID, levelID):
    '''
        Save the floorplan of a level
    '''
    game = GamesList.getByID(gameID)
    level = game.getLevelByID(levelID)
    destination = level.getFloorplanPath()
    if destination.startswith(os.path.sep):
        destination = '.' + destination
    imgData = request.form['imgBase64'].replace('data:image/png;base64,', '')

    try:
        f = open(destination, 'wb')
        f.write(imgData.decode('base64'))
        f.close()
    except IOError as e:
        print e

    return render_template('editLevelFloorplan.html',
        game=game,
        level=level)

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/levels/<int:levelID>/edit')
def editLevel(gameID, levelID):
    '''
        Edit a level
    '''
    game = GamesList.getByID(gameID)
    level = game.getLevelByID(levelID)

    return render_template('levelEditor.html',
        game=game,
        level=level)
