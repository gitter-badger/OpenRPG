import os.path
from flask import Flask, request, send_from_directory

app = Flask(__name__)

@app.route("/")
def showHomepage():
    return send_from_directory(".", "index.html")

@app.route("/game.html")
def showGame():
    return send_from_directory(".", "game.html")

@app.route("/src/<path:path>")
def sendCode(path):
    return send_from_directory("src", path)

@app.route('/games/<path:path>')
def sendGamesFile(path):
    return send_from_directory("games", path)

if __name__ == '__main__':
    app.run()