'''
    This file contains all code related to the games/{{gameID}}/levels directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os
import shutil
from util import *

LEVELS_PATH_BLUEPRINT = Blueprint('LEVELS_PATH_BLUEPRINT', __name__, template_folder='templates')

class Level:
    currentID = -1

    def __init__(self, name, directory):
        self.name = name
        self.directory = os.path.join(directory, self.name.replace(' ', '_'))
        self.configPath = os.path.join(self.directory, 'config.json')
        self.ID = None

    def initFiles(self):
        self.ID = Level.getID()
        os.makedirs(self.directory)
        self.save()

    def load(self):
        try:
            f = open(self.configPath, 'r')
            self.__dict__ = json.load(f)
            f.close()

            if self.ID > Level.currentID:
                Level.currentID = self.ID

        except IOError as e:
            print e

    def save(self):
        try:
            f = open(self.configPath, 'w')
            f.write(json.dumps(self, cls=DictEncoder, indent=3, sort_keys=True))
            f.close()
        except IOError as e:
            print e

    def getDir(self):
        return self.directory

    @staticmethod
    def getID():
        Level.currentID += 1
        return Level.currentID