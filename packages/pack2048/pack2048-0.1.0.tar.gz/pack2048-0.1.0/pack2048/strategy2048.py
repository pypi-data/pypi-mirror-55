#!/usr/bin/env python
# coding: utf-8

## Stratégie

# ## Modifications : augmentation de la vitesse de fusion (fonction snake), prise en compte de la possibilité de fusion avec une ligne supérieure pour la stabilité (stab_line)
# 
# ## TODO : Package, test unitaire, recodage gameover, attention au sens de fusion !

# In[94]:


import random
import numpy
from pack2048.class2048 import *

def process_line_2 (line):
    
    res=[] #ligne à retourner
    r=0 #indice de la prochaine fusion possible
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



def snake_strategy(game,plays, k):
    """
    """
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
    
    def stab_line(game, line):
        list=game[line]
        for i in range (4):
            if list[i]==0:
                return False
            if i!=3 and list[i]==list[i+1]:
                return False
        if True in [list[k]==game[line-1, k] for k in range(len(game[line-1]))]:#on regarde aussi s'il y a une fusion possible
                #avec la ligne supérieure
            return False
            
        return True
    
    def interesting_plays(game):
        """
        """
        K=snake(game)[0]
        if not stab_line(game, 3):
            return [0,3] 
        elif not stab_line(game, 2):
            if K<=4:
                return [0,2,3] 
            elif True in [game[2][k]>=16 for k in range(4)]: 
                return [3,2]
            else:
                return [0,2,3]
        elif not stab_line(game, 1): 
            if K<=8:return [0,2,3]
            elif True in [game[1][k]>=16 for k in range(4)]:
                return [3,0]
            else: return [3,2,0]
        else: return [0,3,2]
       
        
    def val_play(game,k, move):
        """
        """
        g=Game2048(game)
        g.play(move)
        try:
            g.next_turn()
        except( GameOverException, RuntimeError ):
            return snake(game)[1]
        A=[]
        int=interesting_plays(game)
        if k==0:
            return snake(g.game)[1]
        for i in int:
            A.append(val_play(g.game,k-1,i))
        return numpy.max(A)
            

    int=interesting_plays(game)
    score=-20
    move='yolo'
    print (int)
    for i in int:
        
        if val_play(game,k,i)>score:
            move=i
            score=val_play(game,k,i)
    
    return move


## Code et test

# In[104]:




if __name__=="__main__":
    g = Game2048()
    while True:
        d = snake_strategy(g.game, g.moves,5)
        g.play(d)
        try:
            g.next_turn()
        except (GameOverException, RuntimeError):
            break
        print(g.game,d)
        print(g.score())






