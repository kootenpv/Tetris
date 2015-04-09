import numpy as np
import bitarray    

def mergeBoards(args): 
    if isinstance(args, Board):
        args = [args.bits]
    elif isinstance(args, np.ndarray):
        args = [args]
    elif isinstance(args[0], Board):
        args = [x.bits for x in args]
    joiner = np.zeros((args[0].shape[0], 1))
    joiner[0] = True
    new = []
    for arg in args[:-1]:
        new.append(arg)
        new.append(joiner)
    new.append(args[-1])
    print(Board(np.hstack(new)))
        

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
        self.shapes = []
        self.score = self.getDownScore()

    # pylint: disable=E1101 
    def __hash__(self): 
        ba = bitarray.bitarray()
        ba.pack(self.bits.tobytes())
        return hash(ba.tobytes())

    def __repr__(self): 
        outstr = 'd {}  s {}   ch: {}\n'.format(self.depth, self.score, len(self.shapes)) 
        outstr += '-------------------\n' 
        # pylint: disable=W0621
        for x in self.bits:
            for y in x:
                if y:
                    outstr += "o "
                else:    
                    outstr += ". "
            outstr += "\n"
        return outstr + "\n"
        
    def __eq__(self):
        return True
        
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
        # pylint: disable=W0621
        highests = np.argmax(self.bits, 0)
        highests[highests == 0 & np.logical_not(self.bits[0])] = self.board_size[0]
        mask = np.zeros((self.board_size),dtype=bool)
        for i,h in enumerate(highests):
            mask[h:,i] = True
        return(np.sum(mask - self.bits) * self.board_size[1])    
        
    def getDownScore(self): 
        if np.sum(self.bits) == 0:
            return(20,10)
        return(self.getHeightMeasure() - self.getInsideDamage(), 
               self.getLongestLowest())    

