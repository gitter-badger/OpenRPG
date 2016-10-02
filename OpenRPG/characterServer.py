'''
	This file contains all code related to the games/{{game.ID}}/characters directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os
import shutil
from util import *
from Character import Character
from GamesList import GamesList

CHARACTERS_PATH_BLUEPRINT = Blueprint('CHARACTERS_PATH_BLUEPRINT', __name__, template_folder='../templates/characters')

@CHARACTERS_PATH_BLUEPRINT.route('/games/<int:gameID>/characters/new')
def createCharacter(gameID):
    '''
        List all games
    '''
    return render_template('newCharacter.html',
        gameID=gameID)

@CHARACTERS_PATH_BLUEPRINT.route('/games/<int:gameID>/characters/components/manage')
def manageCharacterComponents(gameID):
    '''
        Show the character component manager
    '''

    game = GamesList.getByID(gameID)
    bins = Character.getAllComponentBins(game)

    return render_template('componentManager.html',
        gameID=gameID,
        bins=bins)

@CHARACTERS_PATH_BLUEPRINT.route('/games/<int:gameID>/characters/components/create')
def createCharacterComponent(gameID):
    '''
        Create a character component
    '''

    game = GamesList.getByID(gameID)
    directory = game.getCharacterComponentsDir()
    Character.createCharacterComponentBin(game)
    flash('Created new component bin')

    return redirect(url_for('CHARACTERS_PATH_BLUEPRINT.manageCharacterComponents',
        gameID=gameID))
