# PLAYERS.PY
# Contains an abstract player class and some functions used by it

import numpy as np
import pdb
import random
import Gamestate
import Pieces

def utility(gamestate):
    """Returns a utility vector for a gamestate where 0 is tie, -1 is loss, 1 is win."""
    utilityVector = [-1,-1,-1,-1]
    scores = gamestate.getScores()
    hasHighest = [False,False,False,False]
    hasHighestCount = 0
    highest = scores[0]
    for i in range(1,5):
        if scores[i-1] == highest:
            hasHighest[i-1] = True
            hasHighestCount = hasHighestCount + 1
        if scores[i-1] > highest:
            highest = scores[i-1]
            hasHighest = [False, False, False, False]
            hasHighest[i-1] = True
            hasHighestCount = 1

    if hasHighestCount != 1:
        for i in range(0,4):
            if hasHighest[i]:
                utilityVector[i] = 0
    else:
        for i in range(0,4):
            if hasHighest[i]:
                utilityVector[i] = 1

    return utilityVector  

def expand(gamestate):
    """Expand a gamestate to a list of children."""
    children = list()
    moves = gamestate.listMoves()
    for move in moves:
        new_gamestate = gamestate.duplicate()
        new_gamestate.update(move)
        children.append(new_gamestate)
    return children

def expandFromList(gamestate, moves):
    """Given a list of moves, expand gamestate to corresponding list of children."""
    children = list()
    for move in moves:
        new_gamestate = gamestate.duplicate()
        new_gamestate.update(move)
        children.append(new_gamestate)
    return children

def weightedRandomMove(moves):
    """Return a random move from moves, weighted by piece size."""
    weightedlist = list()
    for move in moves:
        if move != 'pass!':
            for i in range(0, Gamestate.Gamestate.referenceHand[move[0]].size):
                weightedlist.append(move)
        else:
            weightedlist.append('pass!')
                
    return random.choice(weightedlist)

class Player:
    """Abstract player class."""
    def __init__(self, color):
        self.color = color

    def getMove(self, update):
        """When provided a gamestate update, return move"""
        return list()

    def close(self):
        """Perform closing tasks for this AI."""
        pass
        
class AIPlayer(Player):
    """Abstract AI player class."""
    def getMove(self, update):
        #IMPLEMENT THIS
        return list()

class veryStupidAIPlayer(AIPlayer):
    """AI player who makes first move it sees."""
    def getMove(self, update):
        move = update.canMove()
        if move != False:
            return move
        else:
            return 'pass!'

class weightedRandomPlayer(AIPlayer):
    """AI player which makes a random move weighted by piece size"""
    def getMove(self, update):
        moves = update.listMoves()
        move = weightedRandomMove(moves)
        return move
