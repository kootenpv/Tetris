import numpy as np
from .board import Board

generateChildren = {'I' : generateChildrenI,
                    'S' : generateChildrenS,
                    'Z' : generateChildrenZ,
                    'O' : generateChildrenO,
                    'L' : generateChildrenL,
                    'J' : generateChildrenJ,
                    'T' : generateChildrenT}

def generateChildrenI(board, maxChildren):
    #vertical
    children = []
    highests = np.argmax(board.bits, 0)
    highests[highests == 0 & np.logical_not(board.bits[0])] = board.board_size[0]
    for num, i in enumerate(highests * (highests > 3)):

        if i > 0:

            mask = np.zeros(board.board_size, dtype=bool)
            mask[range(i-4,i), num] = True
            b = Board(board.bits | mask, board.depth + 1, board.board_size)
            children.append(b)

    # horizontal
    for i in range(board.board_size[1] - 3):

        if np.all(highests[range(i,i+4)] > 0):

            num = min(highests[range(i,i+4)]) - 1
            mask = np.zeros(board.board_size, dtype=bool)
            mask[num, range(i,i+4)] = True
            b = Board(board.bits | mask, board.depth + 1, board.board_size)
            children.append(b)

    return(sorted(children, key = lambda x: x.score, reverse = True)[:maxChildren])

def generateChildrenO(board, maxChildren):
    children = []
    highests = np.argmax(board.bits, 0)
    highests[highests == 0 & np.logical_not(board.bits[0])] = board.board_size[0]
    doesNotTouchCeiling = (highests * (highests > 1))

    for num, (i, j) in enumerate(zip(doesNotTouchCeiling[:-1], doesNotTouchCeiling[1:])):

        if i > 0 and j > 0:

            ind = min(highests[range(num, num + 2)]) - 1
            mask = np.zeros(board.board_size, dtype=bool)
            mask[ind-1, num] = True
            mask[ind, num] = True
            mask[ind-1, num+1] = True
            mask[ind, num+1] = True
            b = Board(board.bits | mask, board.depth + 1, board.board_size)
            children.append(b)

    return(sorted(children, key = lambda x: x.score, reverse = True)[:maxChildren])

def generateChildrenS():
    children = []
    return children

def generateChildrenZ():
    children = []
    return children

def generateChildrenL():
    children = []
    return children

def generateChildrenJ():
    children = []
    return children

def generateChildrenT():
    children = []
    return children


