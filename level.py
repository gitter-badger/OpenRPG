'''
    This file contains all code related to the games/{{gameID}}/levels directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os
import shutil

LEVELS_PATH_BLUEPRINT = Blueprint('LEVELS_PATH_BLUEPRINT', __name__, template_folder='templates')

class Level:
    currentID = 0

    def __init__(self, name):
        self.name = name
        self.ID = Level.currentID
        Level.currentID += 1

	def load(self):
	    try:
	        f = open(self.configPath, 'r')
	        self.__dict__ = json.load(f)
	        f.close()
	        if self.ID >= Level.currentID:
	        	Level.currentID = self.ID + 1

	    except IOError as e:
	        print e

    def save(self):
        try:
            f = open(self.configPath, 'w')
            f.write(json.dumps(self.__dict__, indent=3, sort_keys=True))
            f.close()
        except IOError as e:
            print e