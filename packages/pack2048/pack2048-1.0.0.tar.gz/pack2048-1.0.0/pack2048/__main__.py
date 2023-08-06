import unittest
import numpy
from pack2048.class2048 import Game2048, evaluate_strategy
from pack2048.strategy2048 import *

class TestStrategy(unittest.TestCase):

    def test_basic(self):
        rnd = snake_strategy(numpy.ones((4, 4), dtype=int), [])
        assert rnd in {0, 1, 2, 3}
        
    
    def test_advanced(self):
        
        mat=numpy.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [8, 4, 2, 2]])
        g=Game2048(mat)
        for i in range(3):
            g.play(snake_strategy(g.game, g.moves, 0))
        self.assertEqual(g.game[3, 0], 16)
        
        mat=numpy.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 4, 0, 0], [8, 4, 2, 2]])
        for i in range(2):
            g.play(snake_strategy(g.game, g.moves, 0))
        self.assertEqual(g.game[3, 0], 16)
        
        mat=numpy.array([[0, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0], [8, 4, 0, 0]])
        g=Game2048(mat)
        g.play(snake_strategy(g.game, g.moves, 0))
        self.assertEqual(g.game[3, 2], 2)
        
        mat=numpy.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 2, 32, 256], [2048, 1024, 512, 128]])
        g=Game2048(mat)
        g.play(snake_strategy(g.game, g.moves, 0))
        self.assertEqual(g.game[2, 0], 2)
        
        mat=numpy.array([[0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 32, 128], [2048, 1024, 512, 256]])
        g=Game2048(mat)
        g.play(snake_strategy(g.game, g.moves, 0))
        self.assertEqual(g.game[2, 1], 2)
             

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