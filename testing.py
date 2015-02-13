
import numpy as np
from Tetris import Board
import random
from Tetris.GameTree import GameTree

def startGame(shapes, turns): 
    board_size = (20, 10)
    GT = GameTree(maxChildren = 3, maxDepth = 2) 
    s = random.choice(shapes)
    a = Board(np.zeros(board_size, dtype=bool), 0) 
    GT.genRoot(a, s)
    options = GT.dealWithNode(a.children)
    for i in range(turns): 
        s = random.choice(shapes)
        GT.genRoot(a, s)         
        options = GT.dealWithNode(a.children) 
        choice = a.children[0][options.index(max(options))]
        print(i,"\n",choice)
        a = Board(choice.bits, 0)
    return(a)    

b = startGame(['I', 'O'], 45)

