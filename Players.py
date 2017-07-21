# PLAYERS.PY
# Contains an abstract player class and human and AI variants with their own
# getMove functions

import numpy as np
import pdb
from Gamestate import *

class Player:
    def __init__(self, color):
        self.color = color

    # when provided updated gamestate, return move
    def getMove(self, update):
        # implement
        return list()

class HumanPlayer(Player):

    def __init__(self, color):
        self.color = color
        self.referenceHand = initRefHand()

    # When provided an updated gamestate, prompt player for their move
    def getMove(self, update):

        # Print information to player
        print("Player" + str(self.color) + ", your hand contains:")
        update.printSortedHand(self.color)

        gotvalidmove = False
        piece_orientation = -1
        move_xmin = -1
        move_ymin = -1
        while not gotvalidmove:
            
            # Prompt player for move
            currHand = update.getHand(self.color)
            name = raw_input("Type name of piece to play, or 'pass' to pass:")
            if name == "pass":
                return list()
            while not currHand[name]:
                name = raw_input("You don't have that piece! Piece to play:")
            coords = np.zeros((2,self.referenceHand[name].size), dtype = int)

            for i in range(0,coords[0].size):
                gotcoordinate = False
                while not gotcoordinate:
                    try:
                        coords[0,i] = int(raw_input("x-coord:"))
                        coords[1,i] = int(raw_input("y-coord:"))
                        if(0 <= coords[0,i] and 19 >= coords[0,i]
                           and 0 <= coords[1,i] and 19 >= coords[1,i]):
                            gotcoordinate = True
                        else:
                            print("Please enter only numbers between 0 and 19")
                    except ValueError as e:
                        print("Please enter valid integers")

            # Check if coordinates match piece claimed, & convert to
            # (piece, orientation, location) form
            piece = self.referenceHand[name]
            piece_orientation = piece.matchingOrientation(coords)
            if piece_orientation == -1:
                print("Those coordinates do not match that piece's shape")
                continue
            
            move_extremes = findExtremes(coords)
            move_xmin, move_ymin = move_extremes[0], move_extremes[2]
            gotvalidmove = True
            
        return (name, piece_orientation, move_xmin, move_ymin)        
    
class AIPlayer(Player):
    def getMove(self, update):
        #IMPLEMENT THIS
        return list()

class veryStupidAIPlayer(Player):
    def getMove(self, update):
        moves = update.listMoves()
        return moves[0]
