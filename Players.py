# PLAYERS.PY
# Contains an abstract player class and human and AI variants with their own
# getMove functions

import numpy as np
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
        self.referenceHand = initHand()

    # When provided an updated gamestate, prompt player for their move
    def getMove(self, update):
        update.printBoard()
        print("Player" + str(self.color) + ", your hand contains:")
        update.printSortedHand(self.color)
        name = raw_input("Type name of piece to play, or 'pass' to pass:")
        if name == "pass":
            return list()
        while not name in self.referenceHand:
            name = raw_input("Invalid name! Piece to play:")
        move = (name, np.zeros((2,self.referenceHand[name].size)))
        
        for i in range(0,move[1][0].size):
            success = False
            while not success:
                try:
                    move[1][0,i] = int(raw_input("x-coord:"))
                    move[1][1,i] = int(raw_input("y-coord:"))
                    if(0 <= move[1][0,i] and 19 >= move [1][0,i]
                       and 0 <= move[1][1,i] and 19 >= move[1][1,i]):
                        success = True
                    else:
                        print("Please enter only numbers between 0 and 19")
                except ValueError as e:
                    print("Please enter valid integers")
        return move
    
class AIPlayer(Player):
    def getMove(self, update):
        #IMPLEMENT THIS
        return list()
