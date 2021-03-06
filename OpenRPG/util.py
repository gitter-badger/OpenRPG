import os, json, time
import unittest
from PIL import Image

class Clock():
    '''
        Used for getting the current time.
        May be deterministically manipulated.
    '''
    def __init__(self):
        self._isMock = False
        self._time = 0

    def getTime(self):
        if self._isMock:
            return self._time

        return time.time()

    def tick(self):
        self._time += 1

    def setTime(self, t):
        self._time = t

    def setMock(self, value):
        self._isMock = value

_clock = Clock()

class Saveable(object):
    '''
        Enables derived classes to save their __dict__s as JSON.
        Important for git compatibility.
    '''
    currentID = 0

    @classmethod
    def nextID(cls):
        result = cls.currentID
        cls.currentID += 1

        return result

    def getDir(self):
        raise NotImplementedError('Savable needs a .getDir() method')
        
    def getSaveFilePath(self):
        return os.path.join(self.getDir(), 'config.json')

    def save(self):
        '''
            Save JSON metadata
        '''
        if not dirExists(self.getDir()):
            os.makedirs(self.getDir())
        try:
            f = open(self.getSaveFilePath(), 'w')
            f.write(json.dumps(self, indent=3, cls=DictEncoder, sort_keys=True))
            f.close()
        except IOError as e:
            print e

    def load(self):
        '''
            Load metadata from self.directory
        '''
        try:
            f = open(self.getSaveFilePath(), 'r')
            values = json.load(f)
            mustSave = False

            for key in self.__dict__:
                if not key in values:
                    # A new key has been added
                    # Save to bring legacy data up to date
                    mustSave = True

            for key in values:
                if key == 'ID':
                    self.__class__.currentID = max(self.__class__.currentID, values['ID'] + 1)
                self.__dict__[key] = values[key] 

            f.close()

            if mustSave:
                self.save()

        except IOError as e:
            print e

class DictEncoder(json.JSONEncoder):
    '''
        Enables the encoding of arbitrary Python objects to JSON
    '''
    def default(self, o):
        d = dict()

        # Ignore "private" fields
        for key in o.__dict__:
            if key[0] != '_':
                d[key] = o.__dict__[key]

        return d

def dirExists(path):
    '''
        Returns true if a directory exists
    '''
    return os.path.exists(path) and os.path.isdir(path)

def listdirs(dirPath):
    '''
        list all subdirectories of a directory
    '''
    return [x for x in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, x))]

def getAllImagesInDir(dirPath):
    '''
        Given a path to a directory,
        Returns a list of paths to all the images in that directory (non-recursive)
    '''
    paths = []

    for path in os.listdir(dirPath):
        if path.endswith('.png'):
            paths.append(os.path.join(dirPath, path))

    return paths

def getIdentifier():
    '''
        Returns the current time as a string
    '''
    return '%.20f' % _clock.getTime()

def nameToDir(name):
    '''
        Takes a name string
        Returns a valid directory name
    '''
    return name.replace(' ', '_')

def createEmptyImage(path, width=64, height=64):
    '''
        Creates an empty png
    '''
    Image.new('RGBA', (width, height)).save(path)