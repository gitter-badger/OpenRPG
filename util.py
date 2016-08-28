import os, json

class Saveable:
    def save(self):
        '''
            Save JSON metadata
        '''
        directory = self.getDir()
        try:
            f = open(os.path.join(directory, 'config.json'), 'w')
            f.write(json.dumps(self, indent=3, cls=DictEncoder, sort_keys=True))
            f.close()
        except IOError as e:
            print e

    def load(self):
        '''
            Load metadata from self.directory
        '''
        try:
            f = open(os.path.join(self.directory, 'config.json'), 'r')
            values = json.load(f)
            mustSave = False

            for key in self.__dict__:
                if not key in values:
                    mustSave = True

            for key in values:
                self.__dict__[key] = values[key] 

            f.close()

            if mustSave:
                self.save()

        except IOError as e:
            print e

class DictEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

def dirExists(path):
    return os.path.exists(path) and os.path.isdir(path)
