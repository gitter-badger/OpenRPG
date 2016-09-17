import unittest
import sys
import os
from shutil import rmtree

sys.path.insert(0, '../OpenRPG')
from OpenRPG.Level import Level
from OpenRPG.util import dirExists

TEMP_DIRECTORY = './tmp'

class test_Level(unittest.TestCase):
    def test_init_delete(self):
        level = Level('_testLevel', TEMP_DIRECTORY)
        level2 = Level('_testLevel', TEMP_DIRECTORY)

        self.assertTrue(os.path.exists(level.getDir()))
        self.assertTrue(os.path.exists(level.getFloorplanPath()))

        for key in level.__dict__:
            self.assertTrue(key in level2.__dict__)
            if key in level2.__dict__:
                self.assertEqual(level.__dict__[key], level2.__dict__[key])

        level.delete()

        self.assertFalse(os.path.exists(level.getDir()))
        self.assertFalse(os.path.exists(level.getFloorplanPath()))


if __name__ == '__main__':
    if not dirExists(TEMP_DIRECTORY):
        os.mkdir(TEMP_DIRECTORY)

    unittest.main()