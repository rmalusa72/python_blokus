# PLAYERS.PY
# Contains an abstract player class and human and AI variants with their own
# getMove functions

import numpy as np
import pdb
import Gamestate
import Pieces

class Player:
    def __init__(self, color):
        self.color = color

    # when provided updated gamestate, return move
    def getMove(self, update):
        # implement
        return list()
        
class AIPlayer(Player):
    def getMove(self, update):
        #IMPLEMENT THIS
        return list()

class veryStupidAIPlayer(AIPlayer):
    def getMove(self, update):
        move = update.canMove()
        if move != False:
            return move
        else:
            return 'pass!'

# Calculate a vector w/utility for each player in a terminal gamestate
# where 0 is in a tie, -1 is a loss, and 1 is a win
def utility(gamestate):
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

# Expands a given gamestate to a list of children
def expand(gamestate):
    children = list()
    moves = gamestate.listMoves()
    for move in moves:
        new_gamestate = gamestate.duplicate()
        new_gamestate.update(move)
        children.append(new_gamestate)
    return children

# Expands a given gamestate to a list of children (given a list of moves)
def expandFromList(gamestate, moves):
    children = list()
    for move in moves:
        new_gamestate = gamestate.duplicate()
        new_gamestate.update(move)
        children.append(new_gamestate)
    return children

