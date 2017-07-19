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
        corners.append(np.array([[-1,0],[-1,0]]))
    if color == 2:
        corners.append(np.array([[-1,0],[boardsize, boardsize-1]]))
    if color == 3:
        corners.append(np.array([[boardsize, boardsize-1],
                                 [boardsize, boardsize-1]]))
    if color == 4:
        corners.append(np.array([[boardsize, boardsize-1],[-1,0]]))
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
        self.boardsize = boardsize
        self.turn = 1

    # Update turn to next player
    def advanceTurn(self):
        self.turn = self.turn + 1
        if self.turn == 5:
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

    # Given a 2x2n matrix of corners, update appropriate color's corner list
    # TO IMPLEMENT: delete corners that point off the board
    def updateCorners(self, color, corners):
        oldList = self.getCorners(color)
        newCorners = corners[0].size / 2
        for i in range(0, newCorners):
            cur = corners[:,2*i:2*(i+1)]
            inv = np.array([[cur[0,1],cur[0,0]],[cur[1,1],cur[1,0]]])
            obliterated = False
            for j in range(0, len(oldList)):
                if np.array_equal(oldList[j],inv):
                    del oldList[j]
                    obliterated = True
                    break
            if -1 in cur or self.boardsize in cur:
                continue
            if not obliterated:
                oldList.append(cur)
                    

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

    # Returns list of possible moves
    # def listMoves(self):
        # implement
    
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
    #def copy(self):
        # IMPLEMENT THIS
