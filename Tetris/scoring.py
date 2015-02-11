import numpy as np

class DownScoring():
    def __init__(self, board_size): 
        self.board_size = board_size
        self.horizontal_length = board_size[1]
    
    def getLongestLowest(self, bits):
        lowest = np.max(np.where(bits)[0])
        tot = np.sum(np.all(bits,1)) * self.horizontal_length
        for n1 in range(self.horizontal_length): 
            if not bits[lowest][n1]:
                c = 1 
                for n2 in range(n1+1, self.horizontal_length):
                    c += 1
                    if bits[lowest][n2]:
                        break
                tot = max(c, tot)            
        return(tot)            

    def getHeightMeasure(bits):
        return(np.min(np.where(bits)[0])) 
        
    def getScore(board): 
        if board.depth == 0:
            return(0)
        return(getHeightMeasure(board.bits), getLongestLowest(board.bits))    
