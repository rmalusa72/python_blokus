# MCTSPLAYERS.PY
# Contains player using Monte Carlo Tree Search and its functions

from Players import *
from MCTree import *
import numpy as np

    
class monteCarloPlayer(AIPlayer):
    def getMove(self, update):
        
        # If this is the first time getMove is called,
        # initialize 'root' and 'current' to opening gamestate
        if not hasattr(self, 'root'):
            self.root = MCNode(update)
        if not hasattr(self, 'current'):
            self.current = self.root

        # Otherwise, determine which moves have been made in order to
        # move 'current' down the tree to the node corresponding to update
        
        # Then repeat Monte Carlo iterations until you run out of time

        # And then pick best move


    # A single runthrough/expansion/playout of the Monte Carlo search tree
    def mcIteration(self):

        # Step through the tree according to upper confidence bounds until we
        # reach a node whose children have not all been explored
        node = self.current
        canStep = self.ucbStep(node)
        while not canStep == False:
            node = canStep
            canStep = self.ucbStep(node)

        # Then expand that node, saving the result (utility vector) of
        # random playout
        result = node.expand()

        # Backpropagate that result through node's parents
        while not node is self.current:
            print("beep")
            node = node.parent
            node.updateStats(result)

    # Given an MCNode, returns the move corresponding to the child with the highest
    # upper confidence bound (for the player at that node)
    # if all children have been explored, or false otherwise
    def ucbStep(self, node):
        if node.fullyExpanded:
            color = node.gamestate.turn
            highestUCB = -1
            highestUCBMove = None
            for move, child in node.children:
                # The upper confidence bound of a node is
                # xi + sqrt(2*ln(n)/ni)
                # where n is total playouts from current gamestate,
                # ni = total playouts from node i,
                # wi = total wins from node i for player color, 
                # and xi = average payout for node i (wi/ni)
                currNodeUCB = (child.wins[color-1]/(child.playouts*1)
                               + np.sqrt(2 * np.log(current.playouts)
                                         / (child.playouts * 1.0)))
                if currNodeUCB > highestUCB:
                    highestUCB = currNodeUCB
                    highestUCBMove = move
            return highestUCBMove
        else:
            return False
