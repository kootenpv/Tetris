
import numpy as np
from Tetris import Board

from Tetris.GameTree import GameTree


max_depth = 5
board_size = (20, 10)

a = Board(np.zeros(board_size, dtype=bool), 0)
GT = GameTree(maxChildren = 3, maxDepth = 2)
GT.genRoot(a, 'I')

options = GT.dealWithNode(a.children)

print(a.children[0][options.index(max(options))])

a = np.zeros(board_size, dtype=bool)
f = 4
a[20-f:20] = True
a[:,1] = False
a[:,2] = False

b = Board(a, 0)
GT = GameTree(maxChildren = 5, maxDepth = 2)
GT.genRoot(b, 'I')




options = GT.dealWithNode(b.children)

print(b.children[0][options.index(max(options))])
