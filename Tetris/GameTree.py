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
      'L' : [[(0,0), (0,1), (1,0), (2,0)],
             [(0,0), (1,0), (1,1), (1,2)],
             [(2,0), (2,1), (1,1), (0,1)],
             [(0,0), (0,1), (0,2), (1,2)]],
      'J' : [[(0,0), (0,1), (1,1), (2,1)],     
             [(0,0), (0,1), (0,2), (1,0)],
             [(0,0), (1,0), (2,0), (2,1)],
             [(1,0), (1,1), (1,2), (0,2)]]
      }        


    def __init__(self, maxOptions, maxDepth):
        self.maxOptions = maxOptions
        self.maxDepth = maxDepth 
        self.max_coordinates = {s : np.max(self.rotations[s], 1) + 1 for s in self.rotations}
        self.it = 0

    def genRoot(self, board, shape):
        self.genChildShape(board, shape)       
        
    def genChild(self, board): 
        if board.depth < self.maxDepth: 
            for s in self.shapes: 
                self.genChildShape(board, s) 

    def genChildShape(self, board, s):
        # In the end it would be 20% faster to just write these out for each piece 
        shapes = []
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
                            shapes.append(b) 
                            doneV.append(i)

        maxOptions = int(self.maxOptions / (board.depth+1))
        shapeOptions = Shape(shapes, maxOptions)
        
        board.shapes.append(shapeOptions)        

    def dealWithNode(self, n):
        self.it += 1
        try:
            if n and n[0].depth == self.maxDepth: 
                return(min([shape.getMaxScore() for shape in n]))
            return(max([[self.dealWithNode(y.shapes) for y in x] for x in n])) 
        except:
            pass
        
    def getTerminalNodes(self, board, container):
        if board.shapes: 
            for x in board.shapes: 
                for y in x.options:
                    self.getTerminalNodes(y, container) 
        else:
            container.append(board)
        return(container)

class Shape():
    def __init__(self, options, maxOptions):
        self.options = options 
        if self.options:
            self.options = sorted(options, key = lambda x: x.score, reverse = True)[:maxOptions] 
            self.depth = self.options[0].depth
    def __iter__(self):
        return iter(self.options)
    def __len__(self):
        return len(self.options)
    def getMaxScore(self):
        return max([option.score for option in self.options])
        
        

# GT = GameTree(10,2)

# a = Board(np.zeros((8,6), dtype=bool))

# GT.genRoot(a, 'I')

# GT.dealWithNode(a.shapes)
