from Pieces import *
import sys
import numpy as np

# Initializes a beginning hand with one of each piece
def initHand():
    rtn = dict()
    rtn['One'] = One()
    rtn['Two'] = Two()
    rtn['I3'] = I3()
    rtn['V3'] = V3()
    rtn['I4'] = I4()
    rtn['L4'] = L4()
    rtn['N4'] = N4()
    rtn['O'] = O()
    rtn['T4'] = T4()
    rtn['F'] = F()
    rtn['I'] = I()
    rtn['L'] = L()
    rtn['N'] = N()
    rtn['P'] = P()
    rtn['T'] = T()
    rtn['U'] = U()
    rtn['V'] = V()
    rtn['W'] = W()
    rtn['X'] = X()
    rtn['Y'] = Y()
    rtn['Z'] = Z()
    return rtn

# Initializes a list with the starting corner for a given player
def startCorner(color, boardsize):
    corners = list()
    if color == 1:
        corners.append(np.array([[0],[0]]))
    if color == 2:
        corners.append(np.array([[0],[boardsize-1]]))
    if color == 3:
        corners.append(np.array([[boardsize-1],[boardsize-1]]))
    if color == 4:
        corners.append(np.array([[boardsize-1],[0]]))
    return corners

# Initializes an empty board of size boardSize
def initBoard(boardSize):
    board = np.zeros((boardSize,boardSize),dtype=int)
    return board

class Gamestate:
    '''Represents a game state in Blokus, with hands and board'''

    # Makes a beginning game state
    def __init__(self, boardsize):
        self.blue = initHand()
        self.yellow = initHand()
        self.red = initHand()
        self.green = initHand()
        self.bcorners = startCorner(1, boardsize)
        self.ycorners = startCorner(2, boardsize)
        self.rcorners = startCorner(3, boardsize)
        self.gcorners = startCorner(4, boardsize)
        self.board = initBoard(boardsize)
        self.turn = 1

    # Returns the hand corresponding to int color    
    def getHand(self, color):
        if color == 1:
            return self.blue
        if color == 2:
            return self.yellow
        if color == 3:
            return self.red
        if color == 4:
            return self.green

    def getCorners(self, color):
        if color == 1:
            return self.bcorners
        if color == 2:
            return self.ycorners
        if color == 3:
            return self.rcorners
        if color == 4:
            return self.gcorners

    # Given a 2xn matrix of coordinates, set those to int color
    def colorSet(self, coords, color):
        if not (color in range(1,5)):
            return False
        for i in range(coords[0].size):
            if self.board[coords[1,i]][coords[0,i]] != 0:
                return False
            self.board[coords[1,i]][coords[0,i]] = color
        return True

    # Returns true if player color can move, false otherwise
    def canMove(self, color):
        if len(self.getHand(color)) == 0:
            return False
        # IMPLEMENT THIS
        return True

    # Print board
    def printBoard(self):
        print self.board
        
    # Print a player's hand
    def printHand(self, i):
        hand = self.getHand(i)
        for name, piece in hand.items():
            sys.stdout.write(name + ' ')
        sys.stdout.write("\n")

    # Copy this gamestate
    def copy(self):
        # IMPLEMENT THIS
