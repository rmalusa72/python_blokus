# MAXNPLAYERS.PY
# Maxn-based players and their functions

import Pieces
import Gamestate
import Players

# Maxn search wrapper which returns the move leading to the best outcome
def maxn_getMove(gamestate, max_score):
    color = gamestate.turn
    moves = gamestate.listMoves()
    children = Players.expandFromList(gamestate, moves)
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
        return Players.utility(gamestate)
    else:
        # Expand to list of child gamestates; do maxn on each and find max
        color = gamestate.turn
        children = Players.expand(gamestate)
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
    
class impracticallyThoroughAIPlayer(Players.AIPlayer):
    def getMove(self, update):
        return maxn_getMove(update, 1)

# X-ply maxn search wrapper that returns the move chosen by x-ply maxn search
def xPlyMaxn_getMove(gamestate, maxdepth, max_score):
    color = gamestate.turn
    moves = gamestate.listMoves()
    children = Players.expandFromList(gamestate, moves)
    if len(children) != 0:
        max_val = -100
        max_val_index = -1
        for i in range(0, len(children)):
            print("testing my move")
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
        print("terminal/reached depth limit")
        return Players.utility(gamestate)
    else:
        color = gamestate.turn
        children = Players.expand(gamestate)
        if len(children) != 0:
            max_val = [-100, -100, -100, -100]
            for child in children:
                print("testing their move")
                score = xPlyMaxn(child, depth + 1, maxdepth, max_score)
                if score[color-1] == max_score:
                    print("pruning")
                    return score
                if score[color-1] > max_val[color-1]:
                    max_val = score
            return max_val
        else:
            child = gamestate.duplicate()
            child.update(list())
            return xPlyMaxn(child, depth + 1, maxdepth, max_score)
    
    
class xPlyAIPlayer(Players.AIPlayer):
    def getMove(self, update):
        return xPlyMaxn_getMove(update, 5, 1)
        
