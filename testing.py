
import cProfile
import numpy as np
from Tetris import Board
import random
from Tetris.GameTree import GameTree
from statistics import mean

def startGame(turns, shapes = None, verbose = True): 
    board_size = (20, 9)
    GT = GameTree(maxChildren = 5, maxDepth = 1)
    if shapes is None:
        shapes = GT.shapes
    a = Board(np.zeros(board_size, dtype=bool), 0) 
    b = Board(np.zeros(board_size, dtype=bool), 0) 
    queue = [random.choice(shapes), random.choice(shapes), random.choice(shapes)]
    for turn in range(turns): 
        GT = GameTree(maxChildren = 5, maxDepth = 2)
        choice = MovePlayer(a, GT, queue, visible = 2, maxDepth = 4)
        GT = GameTree(maxChildren = 20, maxDepth = 1)
        #choice2 = MovePlayer(b, GT, queue, visible = 1, maxDepth = 2)
        choice2 = b
        if verbose:
            print(queue,turn,"\n", Board(np.hstack((choice.bits, np.ones((20,1), dtype=bool), choice2.bits)),0))
        a = Board(choice.bits, 0)
        b = Board(choice2.bits, 0)
        queue.append(random.choice(shapes))
        queue.pop(0)
    return((a, turn))


def MovePlayer(board, GT, queue, visible, maxDepth):
    depths = set(list(range(1, visible + 1)) + [maxDepth])
    for i, d in enumerate(depths):
        GT.maxDepth = d
        for t in GT.getTerminalNodes(board, []): 
            GT.genRoot(t, queue[i])    
    options = GT.dealWithNode(board.children) 
    choice = board.children[0][options.index(max(options))]
    return(choice)




    
def playGames(n = 10, maxTurns = 1000, verbose = True):    
    res = []
    for i in range(n): 
        res.append(startGame(maxTurns, verbose = verbose))
    return(res)    

z=startGame(1000)
    
res3 = playGames(5, 1000, True)

board_size = (20, 10)
GT = GameTree(maxChildren = 10, maxDepth = 2) 
shapes = GT.shapes
a = Board(np.zeros(board_size, dtype=bool), 0) 
for turn in range(turns): 
    s = random.choice(shapes)
    GT.maxDepth = 1
    GT.genRoot(a, s)
    r = random.choice(shapes)
    GT.maxDepth = 2
    for x in a.children[0]:
        GT.genRoot(x, r) 
    options = GT.dealWithNode(a.children) 
    choice = a.children[0][options.index(max(options))]
    print(s,r,turn,"\n",choice)
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

def fn():
    it = 0
    bsize = (20,10)
    maxrow = bsize[0] - 1
    doneV = [] 
    for r in range(maxrow, 2, -1): 
        if len(doneV) == 9:
            break
        for i in range(bsize[1] - 1): 
            if i not in doneV: 
                if bla[r-1][i]:
                    continue
                if bla[r][i+1]:
                    continue
                if bla[r-2][i]:
                    continue
                if bla[r-1][i+1]:
                    continue 
                # match
                mask = np.zeros((bsize), dtype=bool)
                mask[r-1][i] = True
                mask[r][i+1] = True
                mask[r-2][i] = True
                mask[r-1][i+1] = True 
                it += 1
                doneV.append(i)            
    print(it)            
                
                
cProfile.run("for i in range(100000): fn()")


