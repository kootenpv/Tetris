class Board():
    def __init__(self, bits, depth = 0, max_depth = 3, board_size = (20, 10), bestNumChildren = 3):
        self.bits = bits
        if depth == 0:            
            self.score = 0
        else:    
            self.score = self.calculateScore()
        self.depth = depth    
        self.children = []
        self.max_depth = max_depth
        self.board_size = board_size
        self.bestNumChildren = bestNumChildren 
                
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
