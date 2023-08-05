import unittest
import numpy
from pack2048.class2048 import Game2048,evaluate_strategy,random_strategy
from pack2048.strategy2048 import *


class TestStrategy(unittest.TestCase):

    def test_random_strategy(self):
        rnd = random_strategy(numpy.zeros((4, 4), dtype=int))
        assert rnd in {0, 1, 2, 3}

class TestGame(unittest.TestCase):

    def test_game_play(self):
        g = Game2048()
        mat = numpy.zeros((4, 4), dtype=int)
        mat[1, 1] = 1
        g.game=mat
        g.play(0)
        self.assertEqual(g.game[1, 1], 0)
        self.assertEqual(g.game[1, 0], 1)
        self.assertEqual(g.game.ravel().sum(), 1)
        g.play(1)
        self.assertEqual(g.game[1, 0], 0)
        self.assertEqual(g.game[0, 0], 1)
        self.assertEqual(g.game.ravel().sum(), 1)
        g.play(2)
        self.assertEqual(g.game[0, 0], 0)
        self.assertEqual(g.game[0, 3], 1)
        self.assertEqual(g.game.ravel().sum(), 1)
        g.play(3)
        self.assertEqual(g.game[0, 3], 0)
        self.assertEqual(g.game[3, 3], 1)
        self.assertEqual(g.game.ravel().sum(), 1)


if __name__ == '__main__':
    unittest.main()