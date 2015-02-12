import numpy as np
from .board import Board

class GameTree():
    def __init__(self, maxChildren, maxDepth):
        self.maxChildren = maxChildren
        self.maxDepth = maxDepth
        
        self.genChildFunctions = {
            'I' : self.genChildI, 
            #'S' : self.genChildS, 
            #'Z' : self.genChildZ, 
            'O' : self.genChildO, 
            #'L' : self.genChildL, 
            #'J' : self.genChildJ, 
            #'T' : self.genChildT 
        }

    def genRoot(self, board, shape):
        self.genChildFunctions[shape](board)        
        
    def genChild(self, board): 
        if board.depth <= self.maxDepth: 
            for s in self.genChildFunctions:
                self.genChildFunctions[s](board) 

    def genChildI(self, board):
        #vertical 
        children = []
        highests = np.argmax(board.bits, 0)
        highests[highests == 0 & np.logical_not(board.bits[0])] = board.board_size[0]
        for num, i in enumerate(highests * (highests > 3)):

            if i > 0:

                mask = np.zeros(board.board_size, dtype=bool)
                mask[range(i-4,i), num] = True
                b = Board(board.bits | mask, board.depth + 1)
                self.genChild(b)
                children.append(b)

        # horizontal
        for i in range(board.board_size[1] - 3):

            if np.all(highests[range(i,i+4)] > 0):

                num = min(highests[range(i,i+4)]) - 1
                mask = np.zeros(board.board_size, dtype=bool)
                mask[num, range(i,i+4)] = True
                b = Board(board.bits | mask, board.depth + 1)
                self.genChild(b)
                children.append(b)

        children = sorted(children, key = lambda x: x.score, reverse = True)[:self.maxChildren]

        board.children.append(children)

    def genChildO(self, board):
        children = []
        highests = np.argmax(board.bits, 0)
        highests[highests == 0 & np.logical_not(board.bits[0])] = board.board_size[0]
        doesNotTouchCeiling = (highests * (highests > 1))

        for num, (i, j) in enumerate(zip(doesNotTouchCeiling[:-1], doesNotTouchCeiling[1:])):

            if i > 0 and j > 0:

                ind = min(highests[range(num, num + 2)]) - 1
                mask = np.zeros(board.board_size, dtype=bool)
                mask[ind-1, num] = True
                mask[ind, num] = True
                mask[ind-1, num+1] = True
                mask[ind, num+1] = True
                b = Board(board.bits | mask, board.depth + 1) 
                self.genChild(b)
                children.append(b)
                
        children = sorted(children, key = lambda x: x.score, reverse = True)[:self.maxChildren]        
        board.children.append(children)

    def genChildS(self, board):
        children = []
        print("printing not used child board")
        print(board)
        return children

    def genChildZ(self, board):
        children = []
        print("printing not used child board")
        print(board)
        return children

    def genChildL(self, board):
        children = []
        print("printing not used child board")
        print(board)
        return children

    def genChildJ(self, board):
        children = []
        print("printing not used child board")
        print(board)
        return children

    def genChildT(self, board):
        children = []
        print("printing not used child board")
        print(board)
        return children

    def dealWithNode(self, n):
        if n[0][0].depth == self.maxDepth:
            return(min([max([y.score for y in x]) for x in n]))
        return(max([[self.dealWithNode(y.children) for y in x] for x in n])) 
