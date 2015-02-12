import numpy as np

class Board():
    def __init__(self, bits, depth = 0):
        self.bits = bits
        self.depth = depth    
        self.children = []
        self.board_size = bits.shape
        self.score = self.getDownScore() 
                
    def __repr__(self): 
        outstr = 'd {}  s {}   ch: {}\n'.format(self.depth, self.score, len(self.children)) 
        outstr += '-------------------\n'
        for x in self.bits:
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
        return(np.min(np.where(self.bits)[0]) + np.sum(np.all(self.bits,1)))

    def getInsideDamage(self): 
        highests = np.argmax(self.bits, 0)
        highests[highests == 0 & np.logical_not(self.bits[0])] = self.board_size[0]
        mask = np.zeros((self.board_size),dtype=bool)
        for i,h in enumerate(highests):
            mask[h:,i] = True
        return(np.sum(mask - self.bits))    
        
    def getDownScore(self): 
        if self.depth == 0:
            return((0,0))
        return(self.getHeightMeasure() - self.getInsideDamage(), 
               self.getLongestLowest())    
        
