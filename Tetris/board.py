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

import itertools

setje = set()
zzz = []
res = []        
it = 0
for x in itertools.product([0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7]):
    it += 1
    if np.sum(x) % 2 == 0:
        b = np.zeros((8,6), dtype=bool) 
        for num, i in enumerate(x): 
            b[i:, num] = True
        brd = Board(b)     
        hbrd = hash(brd)
        if hbrd not in setje:  
            res.append(brd)
            setje.add(hbrd)
    if it % 1000 == 0:
        print(it)        


from .GameTree import GameTree
        
GT = GameTree(10000, 1)

for num,x in enumerate(res):
    if num % 10000 == 0:
        print(num)
    GT.genChild(x)

class HealthTree():
    def __init__(self, maxOptions, maxDepth):
        self.maxOptions = maxOptions
        self.maxDepth = maxDepth 

    def dealWithNode(self, n):
        if n[0][0].depth == self.maxDepth:
            total = [max([healths[hash(y)] if hash(y) in setje else 0 for y in x]) for x in n]
            return(min(total))
        return(max([[self.dealWithNode(y.shapes) for y in x] for x in n])) 



startGame(100)    


def startGame(turns, shapes = None, verbose = True): 
    board_size = (8, 6) 
    HT = HealthTree(20, 4)
    GT = GameTree(maxOptions = 20, maxDepth = 3) 
    if shapes is None:
        shapes = GT.shapes
    a = Board(np.zeros(board_size, dtype=bool), 0) 
    b = Board(np.zeros(board_size, dtype=bool), 0) 
    samp = Sampler(lookahead = 4)    
    for turn in range(turns): 
        choice = MovePlayer(a, HT, samp, visible = 3, maxDepth = 4)
        #choice2 = MovePlayer(b, GT, samp, visible = 1, maxDepth = 2)
        choice2 = b
        if verbose:
            print(samp.queue,turn,"\n", Board(np.hstack((choice.bits, np.ones((8,1), dtype=bool), choice2.bits)),0))
        a = Board(choice.bits, 0)
        b = Board(choice2.bits, 0)
        piece = samp.consumePiece()
    return((a, turn))

def MovePlayer(board, HT, samp, visible, maxDepth):    
    GT = GameTree(maxOptions = 20, maxDepth = 4) 
    depths = set(list(range(1, visible + 1)) + [maxDepth])
    for i, d in enumerate(depths):
        GT.maxDepth = d
        for t in GT.getTerminalNodes(board, []): 
            GT.genRoot(t, samp.viewNext(i))
    options = HT.dealWithNode(board.shapes) 
    print(max(options))
    choice = board.shapes[0][options.index(max(options))]
    return(choice)
    
startGame(100)        

newres = {}

for x in res:
    it = 0
    for i in x.shapes:
        for j in i:
            if hash(j) in setje:
                it += 1
    newres[hash(x)] = it

hashed_shapes = {}
for x in res:
    legal_shapes = []
    for i in x.shapes:
        tmp = []
        for j in i:
            if hash(j) in setje:
                tmp.append(j)
        legal_shapes.append(tmp)                
    hashed_shapes[hash(x)] = legal_shapes

z = Board(np.ones((8,6), dtype=bool))    

GT.genRoot(z, 'I')

class LegalTree():
    def __init__(self, maxDepth):
        self.maxDepth = maxDepth 
        
    def genChildren(self, board, hashed_shapes_dict): 
        if board.depth < self.maxDepth: 
            if hash(board) in hashed_shapes_dict:
                board.shapes = hashed_shapes_dict[hash(board)]
            else:
                board.shapes = []
            for i in board.shapes:
                for x in i:
                    x.depth = board.depth + 1
                    self.genChildren(x, hashed_shapes_dict)

    def getTerminalNodes(self, board, container):
        if board.shapes: 
            for x in board.shapes: 
                for y in x:
                        self.getTerminalNodes(y, container) 
        else:
            container.append(board)
        return(container)



def MovePlayer(board, HT, samp, visible, maxDepth):    
    GT = GameTree(maxOptions = 20, maxDepth = 4) 
    depths = set(list(range(1, visible + 1)) + [maxDepth])
    for i, d in enumerate(depths):
        GT.maxDepth = d
        for t in GT.getTerminalNodes(board, []): 
            GT.genRoot(t, samp.viewNext(i))
    options = HT.dealWithNode(board.shapes) 
    print(max(options))
    choice = board.shapes[0][options.index(max(options))]
    return(choice)
        

def startGame(turns, verbose = True): 
    board_size = (8, 6) 
    GT = GameTree(maxOptions = 20, maxDepth = 1) 
    LT = LegalTree(2)
    samp = Sampler(lookahead = 5)
    a = Board(np.zeros(board_size, dtype=bool), 0) 
    for turn in range(turns): 
        GT.genRoot(a, samp.viewPiece(0)) 
        for i in a.shapes:
            for x in i:
                LT.genChildren(x, hashed_shapes) 
        options = GT.dealWithNode(a.shapes)
        choice = a.shapes[0].options[options.index(max(options))]
        if verbose:
            print(turn,"\n", choice)
        a = Board(choice.bits, 0)
        piece = samp.consumePiece()
    return((a, turn))
