import random

class Sampler():
    def __init__(self, lookahead = 2, mode='doubleCycle', pieces = ['S', 'Z', 'I' , 'O', 'L' , 'J', 'T']):
        self.pieces = pieces
        self.queue = self.pieces + self.pieces
        random.shuffle(self.queue)
        self.it = -1
        self.lookahead = lookahead
        self.mode = mode

    def getPiece(self): 
        self.it += 1
        if (self.it + self.lookahead) % 14 == 0: 
            newBlock = self.pieces + self.pieces
            random.shuffle(newBlock)
            self.queue.extend(newBlock)
        return(self.queue[self.it])

    def __repr__(self):
        return(str(self.queue))
        
    def __len__(self):    
        return(len(self.queue))

    def viewNext(self, n):
        if n > self.lookahead:
            raise Exception("Cannot look at {}; more than lookahead {}".format(n, self.lookahead))
        return(self.queue[self.it + n]) 
