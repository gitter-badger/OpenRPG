import unittest
import sys
import os
from shutil import rmtree

sys.path.insert(0, '../OpenRPG')
from OpenRPG.Game import Game
from OpenRPG.util import dirExists

Game.GAMES_DIRECTORY = './tmp'

class test_Game(unittest.TestCase):
    def test_initFiles(self):
        game = Game('_testGame')
        game.initFiles()

        self.assertTrue(os.path.exists(game.getDir()))
        self.assertTrue(os.path.exists(game.getLevelsDir()))
        self.assertTrue(os.path.exists(game.getImgDir()))
        self.assertTrue(os.path.exists(game.getCharactersDir()))
        self.assertTrue(os.path.exists(game.getPropsDir()))
        self.assertTrue(os.path.exists(game.getTileDir()))
        self.assertTrue(os.path.exists(game.getAudioDir()))
        self.assertTrue(os.path.exists(game.getMusicDir()))
        self.assertTrue(os.path.exists(game.getSfxDir()))
        self.assertTrue(os.path.exists(game.getCharacterComponentsDir()))

        game.delete()

    def test_save_load(self):
        game = Game('_testGame')
        game.initFiles()
        d1 = game.__dict__

        game2 = Game('_testGame')
        game2.load()
        d2 = game2.__dict__

        for key in d1:
            self.assertTrue(key in d2)
            if key in d2:
                self.assertEqual(d1[key], d2[key])

        game2.delete()

    def test_setTitle(self):
        game = Game('_testGame')
        game.initFiles()

        game.setTitle('_testGame2')

        self.assertEqual(game.getDir(), os.path.join(Game.GAMES_DIRECTORY, '_testGame2'))
        self.assertTrue(os.path.exists(game.getDir()))

        game.delete()

if __name__ == '__main__':
    if not dirExists(Game.GAMES_DIRECTORY):
        os.mkdir(Game.GAMES_DIRECTORY)

    unittest.main()