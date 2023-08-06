
import random
import numpy

__all__=["evaluate_strategy"]

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
        self.game = game if not(game is None) else numpy.zeros((4, 4), dtype=int) 
        self.moves = []

    def __str__(self):

        if len(self.moves) > 3:
            last_moves = self.moves[-3:]
        else:
            last_moves = self.moves
        return "{}\n{}".format(str(self.game), str(last_moves))

    def gameover(self):
        sum=0
        for i in range (4):
            for j in range (4):
                sum+=self.game[i][j]
        if sum==0:
            return False
        if len(self.possible_play())==0:
            return True
        return False

    def copy(self):
        return Game2048(self.game.copy())

    def next_turn(self):
        while True:
            i = random.randint(0, self.game.shape[0] - 1)
            j = random.randint(0, self.game.shape[1] - 1)
            if self.game[i, j] == 0:
                n = random.randint(0, 3)
                self.game[i, j] = 4 if n == 0 else 2
                self.moves.append((i, j, self.game[i, j]))
                break


    def process_line_2 (line):
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
                
    
    def possible_play(self):
        moves=[0,1,2,3]
        pos_moves=[]
        
        
        def not_equal(A,B):
            for i in range(4):
                for j in range(4):
                    if A[i][j]!=B[i][j]:
                        return True
            return False
            
        for i in moves:
            g=Game2048(self.game)
            g.test(i)
            if not_equal(self.game,g.game):
                pos_moves.append(i)
        return pos_moves
    
    
    
    def test(self, direction):
        
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



    def play(self,direction):
        pos_moves=self.possible_play()

        if direction not in pos_moves:
            pos_moves=[]
        else:
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


def evaluate_strategy(fct_strategy, ntries=10):
    for i in range(0, ntries):
        g = Game2048()
        while True:
            g.next_turn()
            d = fct_strategy(g.game, g.moves)
            if g.gameover():
                break
            g.play(d)
        yield g.score()
