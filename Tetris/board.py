import numpy as np

class Board(): 
    def __init__(self, bits, depth = 0): 
        ## remove the lines at initialiation
        self.board_size = bits.shape
        # full_lines = np.all(bits,1)
        # n_full = np.sum(full_lines) 
        # if n_full:
        #     bits = np.delete(bits, np.where(full_lines)[0], 0)            
        #     self.bits = np.vstack((np.zeros((n_full, self.board_size[1]), dtype=bool), bits)) 
        # else:
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

piecesPre = {"S": [[-1], [0, 1]],
             "Z": [[1], [-1, 0]],
             "L": [[0], [0, 0], [0, -1], [-2]],
             "J": [[0], [0, 0], [1, 0], [2]],
             "S": [[0]],
             "I": [[0,0,0], []],
             "T": [   [0,0]      [2,0,0]        , [1], [-1, 1], [-1]]}


pieces = {'S' : [-1], [x+2, -1, -1]}

0,1,2,3


piecesPost = {"S": [[-1], [0, 1]],
             "Z": [],
             "L": [[], [], [], [3, 2, -1]], 
             "J": [],
             "S": [],
             "I": [],
             "T": [[3,1,-1,-1], [3,-2,-1], [-1, 1, 1, -1], [1,2,-2]]}

def heightToBoard(representation = [], depth = 0):
    board_size = (20,10)
    b = np.zeros(board_size, dtype=bool)
    for i in range(board_size[1]): 
        b[:10+sum(representation[:i]), i] = True 
    board = Board(b, depth) 
    print(board)
    return(board)    

z = heightToBoard([0, -2, 2, 0, 0, 0, 0, -2 , 0, 1])
z = heightToBoard([0, 1, 0, -1, 0, 0, 0, -2 , 0, 1])

z = heightToBoard([0, 0, 0, 2, -1, -1, -2 , 0, 1])
z = heightToBoard([1, 1, -1, 1, -1, -1, -2 , 0, 1])

z = heightToBoard([0, 0, 0, 2, -1, -1, -2 , 1, 0])
z = heightToBoard([0, 0, 0, 2, -1, -1, 1 , -1, -1])

z = heightToBoard([0, 0, 0, 2, -1, -2, -1 , 1, 0])
z = heightToBoard([0, 0, 0, 2, -1, -1, 0, 0, -1])

z = heightToBoard([0, 0, 0, 2, -1, -1, 0, -1, 0])
z = heightToBoard([0, 0, 0, 2, -1, -1, 1, 1, -2])



OptionisInContour([0,0], [0, 0, -1, 0, 0, 0, -2 , 0, 1])

flatb = [1, 1, 0, 2, 0, -1, 0, 0, 0]

def OptionisInContour(option, contour):
    possibilities = []
    len_options  = len(option)
    len_contour = len(contour)
    for c in range(len_contour - len_options + 1): 
        if all([contour[i] == option[j] for i,j in zip(range(c, c + len_options), range(len_options))]):
            possibilities.append(c)
    return(possibilities)        
        
            
def genBoards(contour, piece = "T"): 
    b=heightToBoard(contour)
    boards = [] 
    len_contour = len(contour)
    for option, post in zip(piecesPre[piece], piecesPost[piece]): 
        possibilities = OptionisInContour(option, contour)
        for possibility in possibilities: 
            newContour = [] + contour
            len_post = len(post)
            for r, p in zip(range(possibility - 1, possibility + len_contour + 1), post):
                if r > 0 and r < len_contour: 
                    newContour[r] = contour[r] + p
            boards.append(newContour)
    return(boards)        
            

heightToBoard([-3, 2, 0, 0, 0, 0, -2 , 0, 1])

heightToBoard(genBoards([-3, 2, 0, 0, 0, 0, -2 , 0, 1])[3])
        
for i in range(10000):
    z=genBoards([-3, 2, 0, 0, 0, 0, -2 , 0, 1])    


for i in range(100000):
    n = 2
    contour = [-3, 2, 0, 0, 0, 0, -2 , 0, 1]
    m = len(contour) - n + 1
    for i in range(m):
        if contour[i-1:i+n] in piecesPre['T']: 
            ind = piecesPre['T'].index(contour[i-1:i+n])
            middle = piecesPost['T'][ind]
            if i > 0:
                middle[0] += contour[i] 
            z=contour[:i-1] + middle + contour[i+n:]




z = [0, 0, 0, 2, -1, -1, 1, 1, -2]


for i in range(2000000):
    [z[i:i+3] for i in range(8)]

(0,0,1), (1,2,1)
(1,0), ()


for i in range(10000000):
    a = max([2,1,4,6,4,1,134,235,34,535,6,456,45,6,456,45,6])

z=Board(np.zeros((8,6),dtype=bool))    

z.bits[:-5,:1] =  True

