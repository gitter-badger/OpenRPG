import os
from Game import Game

class GamesList:
    '''
        Manages the list of games and ensures unique IDs
    '''
    gamesDirectories = [os.path.join(Game.GAMES_DIRECTORY, x) for x in os.listdir(Game.GAMES_DIRECTORY)]
    games = []

    @staticmethod
    def load(directory):
        '''
            Loads a game from a directory
            Returns the Game
        '''
        return Game.loadFromDirectory(directory)
        
    @staticmethod
    def init():
        '''
            To be called once after creation
            Loads a list of games
        '''
        for directory in GamesList.gamesDirectories:
            GamesList.addGame(GamesList.load(directory))

    @staticmethod
    def addGame(game):
        '''
            Adds a Game to the list
        '''
        GamesList.games.append(game)

    @staticmethod
    def getByID(gameID):
        # TODO: use a hash map to index games
        for i in xrange(len(GamesList.games)):
            game = GamesList.games[i]
            if game.ID == gameID:
                return game

        return None

    @staticmethod
    def removeGame(gameID):
        '''
            Removes a game from the list and deletes it
            Throws: IOError
        '''
        for i in xrange(len(GamesList.games)):
            game = GamesList.games[i]
            if game.ID == gameID:
                game.delete()
                del GamesList.games[i]
                break

    @staticmethod
    def getAllGames():
        '''
            Returns a list of Games
        '''
        GamesList.games.sort()
        return GamesList.games