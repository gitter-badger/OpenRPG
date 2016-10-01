'''
    This file contains all code related to the assets/ directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os
import shutil
from util import *

ASSETS_PATH_BLUEPRINT = Blueprint('ASSETS_PATH_BLUEPRINT', __name__, template_folder='../templates/assets')

@ASSETS_PATH_BLUEPRINT.route('/assets/edit')
def editAsset():
    '''
        Edit tan asset
    '''
    return render_template('bezierEditor.html')