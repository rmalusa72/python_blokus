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

class veryStupidAIPlayer(AIPlayer):
    def getMove(self, update):
        moves = update.listMoves()
        return moves[0]

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

# Maxn search wrapper which returns the move leading to the best outcome
def maxn_getMove(gamestate, max_score):
    color = gamestate.turn
    moves = gamestate.listMoves()
    children = expandFromList(gamestate, moves)
    if len(children) != 0:
        max_val = -100
        max_val_index = -1
        for i in range(0, len(children)):
            score = maxn(children[i], max_score)[color-1]
            if score == max_score:
                return moves[i]
            if score > max_val:
                max_val = score
                max_val_index = i
        return moves[max_val_index]
    else:
        return list()

# Maxn search
# * added immediate pruning
def maxn(gamestate, max_score):
    
    # If gamestate is terminal, return vector of utility
    if gamestate.isTerminal():
        return utility(gamestate)
    else:
        # Expand to list of child gamestates; do maxn on each and find max
        color = gamestate.turn
        children = expand(gamestate)
        if len(children) != 0:
            max_val = [-100,-100, -100, -100]
            for child in children:
                score = maxn(child, max_score)
                # If a child has the best possible score for a player,
                # prune immediately and disregard other children
                if score[color-1] == max_score:
                    return score
                if score[color-1] > max_val[color-1]:
                    max_val = score

            return max_val
        else:
            # If no moves are possible but gamestate is not terminal,
            # simply pass 
            new_gamestate = gamestate.duplicate()
            new_gamestate.update(list())
            return maxn(new_gamestate, max_score)
    
class impracticallyThoroughAIPlayer(AIPlayer):
    def getMove(self, update):
        return maxn_getMove(update, 1)

# X-ply maxn search wrapper that returns the move chosen by x-ply maxn search
def xPlyMaxn_getMove(gamestate, maxdepth, max_score):
    color = gamestate.turn
    moves = gamestate.listMoves()
    children = expandFromList(gamestate, moves)
    if len(children) != 0:
        max_val = -100
        max_val_index = -1
        for i in range(0, len(children)):
            score = xPlyMaxn(children[i], 1, maxdepth, max_score)[color-1]
            if score == max_score:
                return moves[i]
            if score > max_val:
                max_val = score
                max_val_index = i
        return moves[max_val_index]
    else:
        return list()

    
# Maxn search that expands tree to maximum depth of x and then evaluates leaves by current score
def xPlyMaxn(gamestate, depth, maxdepth, max_score):
    print("xPlyMaxn previewing:")
    print(gamestate.board)
    if depth == maxdepth or gamestate.isTerminal():
        return utility(gamestate)
    else:
        color = gamestate.turn
        children = expand(gamestate)
        if len(children) != 0:
            max_val = [-100, -100, -100, -100]
            for child in children:
                score = xPlyMaxn(child, depth + 1, maxdepth, max_score)
                if score[color-1] == max_score:
                    return score
                if score[color-1] > max_val[color-1]:
                    max_val = score
            return max_val
        else:
            child = gamestate.duplicate()
            child.update(list())
            return xPlyMaxn(child, depth + 1, maxdepth, max_score)
    
    
class xPlyAIPlayer(AIPlayer):
    def getMove(self, update):
        return xPlyMaxn_getMove(update, 2, 1)
        
