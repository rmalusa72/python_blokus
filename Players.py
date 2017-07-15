import numpy as np
from Gamestate import *

# Contains an abstract(ish) player class, and the human and AI variants with their own getMove methods

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
        name = raw_input("Piece name:")
        while not name in self.referenceHand:
            name = raw_input("Invalid name! Piece name:")
        move = (name, np.zeros((2,self.referenceHand[name].size)))
        for i in range(0,move[1][0].size):
            move[1][0][i] = int(raw_input("x-coord:"))
            move[1][1][i] = int(raw_input("y-coord:"))
        return move
    
class AIPlayer(Player):
    def getMove(self, update):
        #IMPLEMENT THIS
        return list()
