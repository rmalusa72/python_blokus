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
        move = list()
        name = raw_input("Piece name:")
        while not name in self.referenceHand:
            name = raw_input("Invalid name! Piece name:")
        move.append(name)
        for i in range(0, self.referenceHand[name].size):
            x = int(raw_input("x-coord:"))
            y = int(raw_input("y-coord:"))
            move.append((x,y))
        return move
    
class AIPlayer(Player):
    def getMove(self, update):
        #IMPLEMENT THIS
        return list()
