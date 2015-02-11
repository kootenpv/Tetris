def generateChildren = {
    'T' : generateChildrenO,
    'I' : generateChildrenI,
    'S' : generateChildrenS,
    'Z' : generateChildrenZ,
    'O' : generateChildrenO,
    'L' : generateChildrenL,
    'J' : generateChildrenJ,
    'T' : generateChildrenT
    } 
    
def generateChildrenO(board):
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
            #if np.all(highests[range(i,i+4)] == highests[i]):
            mask = np.zeros(self.board_size, dtype=bool)
            mask[num, range(i,i+4)] = True 
            b = Board(self.bits | mask, self.depth + 1, self.max_depth, self.board_size) 
            
            children.append(b)
            
def generateChildrenI():
    
def generateChildrenS():
    
def generateChildrenZ():
    
def generateChildrenO():
    
def generateChildrenL():
    
def generateChildrenJ():
    
def generateChildrenT():

generateChildrenFunctions[shape](board)



Layer(
    'S' : , [], []
    )


Layer([{I []])


class Tree():
    def generateBoard(self, shape):
        children = [] 
        if self.depth < self.max_depth: 
            if shape == "O": 
                highests = np.argmax(self.bits, 0) 
                highests[highests == 0 & np.logical_not(self.bits[0])] = self.board_size[0]
                doesNotTouchCeiling = (highests * (highests > 1))
                for num, (i, j) in enumerate(zip(doesNotTouchCeiling[:-1], doesNotTouchCeiling[1:])):
                    if i > 0 and j > 0: 
                        ind = min(highests[range(num, num + 2)]) - 1
                        #if highests[num] == highests[num+1]:
                        mask = np.zeros(self.board_size, dtype=bool)
                        mask[ind-1, num] = True
                        mask[ind, num] = True
                        mask[ind-1, num+1] = True
                        mask[ind, num+1] = True
                        b = Board(self.bits | mask, self.depth + 1, self.max_depth, self.board_size) 
                        children.append(b) 
            children.sort(key = lambda s: s.score, reverse=True)
            children = children[:self.bestNumChildren]
            self.children = children

        
