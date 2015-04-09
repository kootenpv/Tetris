import cProfile
import numpy as np
from Tetris import Board
import random
from Tetris.GameTree import GameTree



def startGame(turns, shapes = None): 
    board_size = (20, 10)
    GT = GameTree(maxChildren = 5, maxDepth = 2) 
    if shapes is None:
        shapes = GT.shapes
    s = random.choice(shapes) 
    a = Board(np.zeros(board_size, dtype=bool), 0) 
    GT.genRoot(a, s)
    options = GT.dealWithNode(a.children)
    for turn in range(turns): 
        s = random.choice(shapes)
        GT.genRoot(a, s)         
        options = GT.dealWithNode(a.children) 
        choice = a.children[0][options.index(max(options))]
        print(turn,"\n",choice)
        a = Board(choice.bits, 0)
    return(a)    

b = startGame(50)

board_size = (20, 10)
GT = GameTree(maxChildren = 10, maxDepth = 2) 
shapes = GT.shapes
s = random.choice(shapes) 
a = Board(np.zeros(board_size, dtype=bool), 0) 
GT.genRoot(a, s)
options = GT.dealWithNode(a.children)
turn = 0
while True:
    turn += 1
    s = random.choice(shapes)
    GT.genRoot(a, s)         
    options = GT.dealWithNode(a.children)
    choice = a.children[0][options.index(max(options))]
    print('turn {} shape {} gamestate {}\n'.format(turn,s,choice))
    a = Board(choice.bits, 0)



# s horizontal
def fn():
    bsize = (20,10)
    maxrow = bsize[0] - 1
    doneV = [] 
    for r in range(maxrow, 1, -1): 
        if len(doneV) == 8:
            return
        for i in range(bsize[1] - 2): 
            if i not in doneV: 
                if bla[r][i]:
                    continue
                if bla[r][i+1]:
                    continue
                if bla[r-1][i+1]:
                    continue
                if bla[r-1][i+2]:
                    continue 
                # match
                mask = np.zeros((bsize), dtype=bool)
                mask[r][i] = True
                mask[r][i+1] = True
                mask[r-1][i+1] = True
                mask[r-1][i+2] = True 
                doneV.append(i)

        
