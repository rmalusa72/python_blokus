# MAXNPLAYERS.PY
# Maxn-based players and their functions

import Pieces
import Gamestate
import Players

def maxn_getMove(gamestate, max_score):
    """Wrapper for maxn search - return result of search."""
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

# NOTE: added immediate pruning
def maxn(gamestate, max_score):
    """Return result of maxn search for best outcome."""
    
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
    """AI player which attempts a complete maxn search."""
    def getMove(self, update):
        return maxn_getMove(update, 1)

def xPlyMaxn_getMove(gamestate, maxdepth, max_score):
    """Wrapper for x-ply maxn search - return result of search."""
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

def xPlyMaxn(gamestate, depth, maxdepth, max_score):
    """Return result of x-ply maxn search for best outcome."""
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
    """AI player who uses x-ply maxn search to find moves."""
    def getMove(self, update):
        return xPlyMaxn_getMove(update, 5, 1)
        
