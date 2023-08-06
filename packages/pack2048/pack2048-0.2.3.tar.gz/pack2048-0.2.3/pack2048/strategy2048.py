import random
import numpy

from pack2048.class2048 import Game2048, GameOverException, evaluate_strategy

__all__=["snake_strategy"]

def snake_strategy(game,plays=[],k=5):
    def snake (game): 
        A=game[2][::-1]
        B=game[0][::-1]
        snake=[]
        snake.extend( game[3])
        snake.extend(A)
        snake.extend(game[1])
        snake.extend( B)
        k=1
        s=snake[0]
        while k<16 and snake[k]<=snake[k-1]:
            if snake[k]==snake[k-1]:
                s+=snake[k]/2 #favoriser la fusion
                k+=1
            else:
                s+=snake[k]
                k+=1
        return k,s
    def nombre_zeros(game):
        nb=0 
        for i in range(4):
            for j in range(4):
                if game[i][j]==0:
                    nb+=1
        return nb
    
    def ligne_stable(list):
        for i in range (4):
            if list[i]==0:
                return False
            if i!=3 and list[i]==list[i+1]:
                return False
        return True
    
    def interesting_plays(game):
        K=snake(game)[0]
        if not ligne_stable(game[3]):
            return [0,3]
        elif not ligne_stable(game[2]):
            if K<=4:
                return [0,2,3]
            elif game[2][3]>=16:
                return [3,2]
            else:
                return [2,0,3]
        elif not ligne_stable(game[1]):
            if K<=8:return [0,2,3]
            elif game[1][0]>=16:
                return [3,0]
            else: return [3,2,0]
        else: return [0,3,2]
        
    def val_play(game,k,move):
        g=Game2048(game)
        g.play(move)
        g.next_turn()
        if g.gameover():
            return 0
        A=[]
        int=interesting_plays(g.game)
        pos_play=g.possible_play()
        ob=intersection(int,pos_play)
        if len(ob)==0:
            ob=pos_play
        if g.score()<512:
            if len(ob)==0:
                return snake(g.game)[1]
            if k==0:
                return snake(g.game)[1]
            
        else:
            if len(ob)==0:
                return snake(g.game)[1] +2**nombre_zeros(g.game)
            if k==0:
                return snake(g.game)[1] +2**nombre_zeros(g.game)
        for i in ob:
            A.append(val_play(g.game,k-1,i))
        return numpy.max(A)
            
    def intersection (a,b):
        res=[]
        for i in a:
            if i in b:
                res.append(i)
        return res
        
        
    int=interesting_plays(game)
    g=Game2048(game)
    pos_play=g.possible_play()
    ob=intersection(int,pos_play)
    if len(ob)==0:
        ob=pos_play
    
    score=-20
    move='yolo'
    for i in ob:
        if val_play(game,k,i)>score:
            move=i
            score=val_play(game,k,i)
    return move



if __name__=='__main__':
    g = Game2048()
    while True:
        g.next_turn()
        d = snake_strategy(g.game, g.moves,5)
        g.play(d)
        if g.gameover():
            break
        print(g.game,d)
    print(g.score())