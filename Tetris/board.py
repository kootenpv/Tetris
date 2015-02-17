import numpy as np

class Board(): 
    def __init__(self, bits, depth = 0): 
        ## remove the lines at initialiation
        self.board_size = bits.shape
        full_lines = np.all(bits,1)
        n_full = np.sum(full_lines) 
        if n_full:
            bits = np.delete(bits, np.where(full_lines)[0], 0)            
            self.bits = np.vstack((np.zeros((n_full, self.board_size[1]), dtype=bool), bits)) 
        else:
            self.bits = bits    
        self.depth = depth    
        self.children = [] 
        self.score = self.getDownScore() 
        
    def reset(self):        
        self.depth = 0
        self.bits[:] = False
                
    def __repr__(self): 
        outstr = 'd {}  s {}   ch: {}\n'.format(self.depth, self.score, len(self.children)) 
        outstr += '-------------------\n'
        for x in reversed(self.bits):
            for y in x:
                if y:
                    outstr += "o "
                else:    
                    outstr += ". "
            outstr += "\n"
        return outstr + "\n"   

    def getLongestLowest(self):
        lowest = np.max(np.where(self.bits)[0])
        tot = np.sum(np.all(self.bits,1)) * self.board_size[1]
        for n1 in range(self.board_size[1]): 
            if not self.bits[lowest][n1]:
                c = 1 
                for n2 in range(n1+1, self.board_size[1]):
                    c += 1
                    if self.bits[lowest][n2]:
                        break
                tot = max(c, tot)            
        return(tot)            

    def getHeightMeasure(self):
        return(np.min(np.where(self.bits)[0]))

    def getInsideDamage(self): 
        highests = np.argmax(self.bits, 0)
        highests[highests == 0 & np.logical_not(self.bits[0])] = self.board_size[0]
        mask = np.zeros((self.board_size),dtype=bool)
        for i,h in enumerate(highests):
            mask[h:,i] = True
        return(np.sum(mask - self.bits) * self.board_size[1])    

    def numHoles(self):
        true_bits = np.where(self.bits)        
        holes = 0
        done = set()
        y, x = true_bits
        for a,b in zip(x,y):
            if a in done:
                continue
            for i in range(b, self.board_size[0]):
                if not self.bits[(i, a)]:
                    holes += 1
            done.add(a)
        return(holes)    

    def getDownScore(self): 
        if np.sum(self.bits) == 0:
            return(20,10)
        #self.getHeightMeasure()
        return( - self.getInsideDamage() - self.numHoles(), 
               self.getLongestLowest())    


(-1)              2
(1)               2
(0,1)             1
(-1,0)            1
(1, -1)           1
(0)               3
(0,0)             3
(1,0)             1
(-1,0)            1
(2)               1
(-2)              1  
(0,0,0)           1
()                1

S: (-1), (0, 1)
Z: (1), (-1, 0)
L: (0), (0, 0), (1, 0), (2)
J: (0), (0, 0), (0, -1), (-2)
S: (0)
I: (0,0,0), () # empty set
T: (0,0), (1), (1, -1), (-1) 


(-1,0,1)

def heightToBoard(representation = [], initialHeight = 0, depth = 0):
    board_size = (20,10)
    b = np.zeros(board_size, dtype=bool)
    for i in range(board_size[1]): 
        print(initialHeight , sum(representation[:i]))
        b[:initialHeight + sum(representation[:i]), i] = True
        print(b)
    board = Board(b, depth)    
    return(board)    

heightToBoard([0, 1, 0, 2, 0, 1, 0, 0, 0], 10)    
