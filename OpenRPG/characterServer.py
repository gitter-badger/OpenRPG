'''
	This file contains all code related to the games/{{game.ID}}/characters directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os
import shutil
from Level import Level
from Game import *
from GamesList import GamesList
from util import *
import glob

CHARACTERS_PATH_BLUEPRINT = Blueprint('CHARACTERS_PATH_BLUEPRINT', __name__, template_folder='../templates/characters')

@CHARACTERS_PATH_BLUEPRINT.route('/games/<int:gameID>/characters/new')
def createCharacter(gameID):
    '''
        List all games
    '''
    return render_template("newCharacter.html",
        gameID=gameID)
