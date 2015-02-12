import numpy as np

class Board():
    def __init__(self, bits, depth = 0, board_size = (20, 10)):
        self.bits = bits
        self.depth = depth    
        self.children = []
        self.board_size = board_size
        self.score = self.getDownScore() 
                
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
        
    def getDownScore(self): 
        if self.depth == 0:
            return(0)
        return(self.getHeightMeasure(), 
               self.getLongestLowest())    
        
