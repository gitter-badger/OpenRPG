'''
    This file contains all code related to the games/{gameID}/levels directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os
import shutil
from Level import Level
from Game import *
from GamesList import GamesList
from util import *

LEVELS_PATH_BLUEPRINT = Blueprint('LEVELS_PATH_BLUEPRINT', __name__, template_folder='../templates/levels')


@LEVELS_PATH_BLUEPRINT.route('/games/<int:gameID>/levels/new', methods=['POST'])
def createLevel(gameID):
    '''
        Create a new level
    '''
    levelName = Level.getUniqueLevelName()
    GamesList.getByID(gameID).addLevel(levelName)

    return redirect(url_for('GAMES_PATH_BLUEPRINT.editGame',
        gameID=gameID))

@LEVELS_PATH_BLUEPRINT.route('/games/<int:gameID>/levels/<int:levelID>/delete', methods=['POST'])
def deleteLevel(gameID, levelID):
    '''
        Delete a level
    '''
    GamesList.getByID(gameID).deleteLevel(levelID)

    flash("Level deleted")

    return redirect(url_for('GAMES_PATH_BLUEPRINT.editGame',
        gameID=gameID))

@LEVELS_PATH_BLUEPRINT.route('/games/<int:gameID>/levels/<int:levelID>/floorplan/edit')
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

@LEVELS_PATH_BLUEPRINT.route('/games/<int:gameID>/levels/<int:levelID>/floorplan/save', methods=['POST'])
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
        level.updateFloorplanImageId()
        flash('Saved level floorplan')
    except IOError as e:
        flash('Error: Failed to save floorplan')
        print e

    return redirect(url_for('GAMES_PATH_BLUEPRINT.editGame',
        gameID=gameID))

@LEVELS_PATH_BLUEPRINT.route('/games/<int:gameID>/levels/<int:levelID>/edit')
def editLevel(gameID, levelID):
    '''
        Edit a level
    '''
    game = GamesList.getByID(gameID)
    level = game.getLevelByID(levelID)

    return render_template('levelEditor.html',
        game=game,
        level=level)