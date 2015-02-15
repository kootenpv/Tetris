import numpy as np
from .board import Board

class GameTree():
    shapes = ['I', 'O', 'S', 'Z', 'T', 'L', 'J']
    
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
    # weird l and j       
          'L' : [[(0,0), (0,1), (0,2), (1,0)],
                 [(0,0), (0,1), (1,0), (2,0)]],
          'J' : [[(0,0), (0,1), (0,2), (1,2)],
                 [(0,0), (1,0), (2,0), (2,1)]]
          }

    def __init__(self, maxChildren, maxDepth):
        self.maxChildren = maxChildren
        self.maxDepth = maxDepth 
        self.max_coordinates = {s : np.max(self.rotations[s], 1) + 1 for s in self.rotations}

    def genRoot(self, board, shape):
        self.genChildShape(board, shape)       
        
    def genChild(self, board): 
        if board.depth < self.maxDepth: 
            for s in self.shapes: 
                self.genChildShape(board, s) 

    def genChildShape(self, board, s):
        # In the end it would be 20% faster to just write these out for each piece 
        children = []
        for rotation, max_sizes in zip(self.rotations[s], self.max_coordinates[s]): 
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
                            b = Board(board.bits | mask, board.depth + 1)
                            self.genChild(b)
                            children.append(b)    
                            doneV.append(i) 

        maxChildren = int(self.maxChildren / (board.depth+1))
        children = sorted(children, key = lambda x: x.score, reverse = True)[:maxChildren]
        
        board.children.append(children)        

    def dealWithNode(self, n):
        if n[0][0].depth == self.maxDepth:
            return(min([max([y.score for y in x]) for x in n]))
        return(max([[self.dealWithNode(y.children) for y in x] for x in n])) 
