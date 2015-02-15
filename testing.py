
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


fn()


rotations = {'S' : [[(0,0), (0,1), (1,1), (1,2)],
                 [(1,0), (0,1), (2,0), (1,1)]],
          'I' : [[(0,0), (0,1), (0,2), (0,3)],
                 [(0,0), (1,0), (2,0), (3,0)]],
          'O' : [[(0,0), (0,1), (1,0), (1,1)]],
          'T' : [[(0,0), (0,1), (0,2), (1,1)],
                 [(0,0), (1,0), (2,0), (1,1)],
                 [(0,1), (1,0), (1,1), (1,2)],
                 [(1,0), (0,1), (1,1), (2,1)]],
          'Z' : [[(1,0), (1,1), (0,1), (0,2)], 
                 [(0,0), (1,0), (1,1), (2,1)]],
          'L' : [[(0,0), (0,1), (0,2), (1,0)],
                 [(0,0), (0,1), (1,0), (2,0)]],
          'J' : [[(0,0), (0,1), (0,2), (1,2)],
                 [(0,0), (1,0), (2,0), (2,1)]]
          }

max_coordinates = {s : np.max(rotations[s], 1) + 1 for s in rotations}

def genChild(board, s): 
    for rotation, max_sizes in zip(rotations[s], max_coordinates[s]): 
        doneV = []
        for r in range(board.board_size[0] - 1, - 2 + max_sizes[0], -1): 
            if len(doneV) == board.board_size[1] - max_sizes[1] + 1:
                break
            for i in range(board.board_size[1] - max_sizes[1] + 1): 
                if i not in doneV:
                    for c in rotation: 
                        if board.bits[r - c[0]][i + c[1]]:
                            break
                    else:    
                        mask = np.zeros((board.board_size), dtype=bool)    
                        for c in rotation:
                            mask[r - c[0]][i + c[1]] = True
                        doneV.append(i) 

genChild(a,'S')
        
