"""
Implements the rule the 2048 game.
"""
import random
import numpy

__all__=["evaluate_strategy","random_strategy"]

class GameOverException(RuntimeError):
    """
    Raised when the game is over.
    """
    pass


class Game2048:
    """
    Implements the logic of the game 2048.
    """

    def __init__(self, game=None):
        """
        :param game: None or matrix 4x4
        """
        self.game = game if not(game is None) else numpy.zeros((4, 4), dtype=int)
        self.moves = []

    def __str__(self):
        "Displays the game as a string."
        if len(self.moves) > 3:
            last_moves = self.moves[-3:]
        else:
            last_moves = self.moves
        return "{}\n{}".format(str(self.game), str(last_moves))

    def gameover(self):
        return numpy.ma.masked_not_equal(self.game, 0).count() == 0
         #gameover s'il n'y a plus de mouvements possibles

    def copy(self):
        "Makes a copy of the game."
        return Game2048(self.game.copy())

    def next_turn(self):
        "Adds a number in the game."
        if self.gameover():
            raise GameOverException("Game Over\n" + str(self.game))
        else:
            while True:
                i = random.randint(0, self.game.shape[0] - 1)
                j = random.randint(0, self.game.shape[1] - 1)
                if self.game[i, j] == 0:
                    n = random.randint(0, 3)
                    self.game[i, j] = 4 if n == 0 else 2
                    self.moves.append((i, j, self.game[i, j]))
                    break

    @staticmethod
    def process_line_2 (line): #[0, 0, 2, 2] -> [2, 2, 0, 0] -> [4, 0, 0, 0] -> [0, 0, 0, 4]
        res=[]      
        r=0 
        for n in line:
            if n==0 :
                continue
            if len(res)==0:
                res.append(n) 
            else:
                if len(res)==r:
                    res.append(n)
                else:
                    if n==res[-1]:
                        res[-1]=2*n
                        r+=1
                    else:
                        res.append(n)
                        r+=1
        while len(res)<len(line):
            res.append(0)
        return res
                

    def play(self, direction):
        "Updates the game after a direction was chosen."
        if direction == 0:
            lines = [Game2048.process_line_2(self.game[i])
                     for i in range(4)]
            self.game = numpy.array(lines)
        elif direction == 1:
            lines = [Game2048.process_line_2(self.game.T[:][i])
                     for i in range(4)]
            
            self.game = numpy.array(lines).T
        elif direction == 2:
            lines = [list(reversed(Game2048.process_line_2(self.game[i] [::-1])))
                     for i in range(4)]
            self.game = numpy.array(lines)
        elif direction == 3:
            lines = [list(reversed(Game2048.process_line_2(self.game.T[i][ ::-1])))
                     for i in range(4)]
            self.game = numpy.array(lines).T

    def score(self):
        return numpy.max(self.game)

    def best_move(self, game=None, moves=None):
        """
        Selects the best move knowing the current game.
        By default, selects a random direction.
        This function must not modify the game.

        :param game: 4x4 matrix or None for the current matrix
        :param moves: all moves since the begining
        :return: one integer
        """
        if game is None:
            game = self.game
        if moves is None:
            moves = self.moves
        if moves is None:
            raise ValueError("moves cannot be None")
        if not isinstance(game, numpy.ndarray) or game.shape != (4, 4):
            raise ValueError("game must be a matrix (4x4).")
        return random.randint(0, 3)


"""
Implements a random strategy for the game 2048.
"""


def random_strategy(game, moves=None):
    return random.randint(0, 3)


def random_strategy_all_but_one(game, moves=None):
    """
    Returns a random direction among three.

    :param game: matrix usually 4x4 but could anything else
    :param moves: list of previous moves (unused)
    :return: a direction in `{0, 1, 2}`
    """
    return random.randint(0, 2)



def evaluate_strategy(fct_strategy, ntries=10):
    for i in range(0, ntries):
        g = Game2048()
        while True:
            try:
                g.next_turn()
            except (GameOverException, RuntimeError):
                break
            d = fct_strategy(g.game, g.moves)
            g.play(d)
        yield g.score()