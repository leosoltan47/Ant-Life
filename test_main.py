import unittest
from main import GameBoard

class TestMain(unittest.TestCase):
    def testInitGameBoard(self):
        Game: GameBoard = GameBoard(4, 4)
        self.assertEqual(Game.width, 4)
        self.assertEqual(Game.height, 4)
        self.assertNotEqual(Game.world, None)

if __name__ == "__main__":
    unittest.main()
