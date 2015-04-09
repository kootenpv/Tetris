### COMES FROM BOARD.PY

import itertools

setje = set()
zzz = []
res = []        
it = 0
for x in itertools.product(*[[0,1,2,3,4,5,6,7]] * 6):
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







     
