from Pieces import *
import sys

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

# Initializes an empty board of size boardSize
def initBoard(boardSize):
    board = list()
    for i in range(boardSize):
        board.append(list())
        for j in range(boardSize):
            board[i].append(0)
    return board

class Gamestate:
    '''Represents a game state in Blokus, with hands and board'''

    # By default makes a beginning game state, or uses provided parameters
    def __init__(self, blue = initHand(), red = initHand(), yellow = initHand(), green = initHand(), board = initBoard(20), turn = 1):
        self.blue = blue
        self.red = red
        self.yellow = yellow
        self.green = green
        self.board = board
        self.turn = turn

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

    # Given a list of tuple coordinates, set those to int color
    def colorSet(self, coords, color):
        if not (color in range(1,5)):
            return False
        for i in range(len(coords)):
            if self.board[coords[i][0]][coords[i][1]] != 0:
                return False
            self.board[coords[i][0]][coords[i][1]] = color
        return True

    # Returns true if player color can move, false otherwise
    def canMove(self, color):
        if len(self.getHand(color)) == 0:
            return False
        # IMPLEMENT THIS
        return True

    # Function to print board
    def printBoard(self):
        for i in range(len(self.board[0])):
            for j in range(len(self.board)):
                sys.stdout.write(str(self.board[j][i]) + ' ')
            print('\n')


        
