import os, json

class DictEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

def dirExists(path):
    return os.path.exists(path) and os.path.isdir(path)