
import numpy as np
import time
        
class Board():
    def __init__(self, bits, depth = 0, max_depth = 3, board_size = (20, 10)):
        self.bits = bits
        if depth == 0:            
            self.score = 0
        else:    
            self.score = self.calculateScore()
        self.depth = depth    
        self.children = []
        self.max_depth = max_depth
        self.board_size = board_size
        
    def generateBoard(self, shape):
        children = []
        if self.depth < self.max_depth: 
            if shape == "I": 
                #vertical 
                highests = np.argmax(self.bits, 0) 
                highests[highests == 0 & np.logical_not(self.bits[0])] = self.board_size[0] 
                for num, i in enumerate(highests * (highests > 3)): 
                    if i > 0:
                        mask = np.zeros(self.board_size, dtype=bool)
                        mask[range(i-4,i), num] = True
                        b = Board(self.bits | mask, self.depth + 1, self.max_depth, self.board_size) 
                        children.append(b)
                # horizontal        
                for i in range(self.board_size[1] - 3):
                    if np.all(highests[range(i,i+4)] > 0):
                        num = min(highests[range(i,i+4)]) - 1
                        if np.all(highests[range(i,i+4)] == highests[i]):
                            mask = np.zeros(self.board_size, dtype=bool)
                            mask[num, range(i,i+4)] = True 
                            b = Board(self.bits | mask, self.depth + 1, self.max_depth, self.board_size) 
                            children.append(b)
            if shape == "O": 
                highests = np.argmax(self.bits, 0) 
                highests[highests == 0 & np.logical_not(self.bits[0])] = self.board_size[0]
                doesNotTouchCeiling = (highests * (highests > 1))
                for num, (i, j) in enumerate(zip(doesNotTouchCeiling[:-1], doesNotTouchCeiling[1:])):
                    if i > 0 and j > 0: 
                        ind = min(highests[range(num, num + 2)]) - 1
                        if highests[num] == highests[num+1]:
                            mask = np.zeros(self.board_size, dtype=bool)
                            mask[ind-1, num] = True
                            mask[ind, num] = True
                            mask[ind-1, num+1] = True
                            mask[ind, num+1] = True
                            b = Board(self.bits | mask, self.depth + 1, self.max_depth, self.board_size) 
                            children.append(b) 
        return(children)                
    def __str__(self):
        outstr = ""
        for x in self.bits:
            for y in x:
                if y:
                    outstr += "o "
                else:    
                    outstr += ". "
            outstr += "\n"
        return outstr            

    def countChildren(self, num = 0):
        for x in self.children:
            num = x.countChildren(num)
        return num + len(self.children)   

    def countChildren(self, num = 0):
        for x in self.children:
            num = x.countChildren(num)
        return num + len(self.children)   
        
    def printTerminalNodes(self):
        for x in self.children:
            x.printTerminalNodes()
            if not x.children:
                print(x)
                
    def calculateScore(self):
        return(np.min(np.where(self.bits)[0]), getLongestLowest(self.bits))
        

n = 100
board_size = (20, 10)
a = Board(np.zeros(board_size, dtype=bool), 0, 5, board_size)
children = []
children.extend(a.generateBoard("O")[:n])
children.extend(a.generateBoard("I")[:n])
a.children = children
a.children.sort(key=lambda s: s.score, reverse=True)
for x in a.children: 
    children = []
    children.extend(x.generateBoard("O")[:n])
    children.extend(x.generateBoard("I")[:n])
    x.children = children
    x.children.sort(key=lambda s: s.score, reverse=True)
    for y in x.children:
        children = []
        children.extend(y.generateBoard("O")[:n])
        children.extend(y.generateBoard("I")[:n])
        y.children = children
        y.children.sort(key=lambda s: s.score, reverse=True)
        for z in y.children:
            children = []
            children.extend(z.generateBoard("O")[:n])
            children.extend(z.generateBoard("I")[:n])
            z.children = children
            z.children.sort(key=lambda s: s.score, reverse=True)
                
a.countChildren()


print(z)

def getLongestLowest(bits):
    horizontal_length = bits.shape[1]
    lowest = np.max(np.where(bits)[0])
    tot = np.sum(np.all(bits,1)) * horizontal_length
    for n1 in range(horizontal_length): 
        if not bits[lowest][n1]:
            c = 1 
            for n2 in range(n1+1, horizontal_length):
                c += 1
                if bits[lowest][n2]:
                    break
            tot = max(c, tot)            
    return(tot)            
