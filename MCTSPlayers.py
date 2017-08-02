# MCTSPLAYERS.PY
# Contains player using Monte Carlo Tree Search and its functions

from Players import *
import random

def randomMove(gamestate):
    moves = gamestate.listMoves()
    return random.choice(moves)
    
class monteCarloPlayer(AIPlayer):
    def getMove(self, update):
        x = 10
