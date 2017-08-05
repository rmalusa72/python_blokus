# MCTSPLAYERS.PY
# Contains player using Monte Carlo Tree Search and its functions

from Players import *
from MCTree import *
import numpy as np

    
class monteCarloPlayer(AIPlayer):
    def getMove(self, update):
        
        # If this is the first time getMove is called,
        # initialize 'root' and 'current' to node w/ opening gamestate
        # and set 'prev' to opening gamestate for future comparisons to
        # determine what move was made
        if not hasattr(self, 'root'):
            self.root = MCNode(update)
            self.current = self.root
            self.prev = update

        # Otherwise, determine which moves have been made by each player in order to
        # move 'current' down the tree to the node corresponding to update
        else:
            colorToCheck = self.color + 1
            if colorToCheck == 5:
                colorToCheck = 1
            while True:

                # Find move made by player, then move down tree to corresponding
                # node, or create it if necessary
                moveMade = self.findMoveMade(self.prev, update, colorToCheck)
                print(moveMade)
                if moveMade in self.current.children:
                    self.current = self.current.children[moveMade]
                else:
                    self.current.children[moveMade] = MCNode(moveMade, parent = self.current)
                    self.current = self.current.children[moveMade]

                # Go to next player in order
                colorToCheck = colorToCheck + 1
                if colorToCheck == 5:
                    colorToCheck = 1
                if colorToCheck == self.color:
                    break
        
        # Then repeat Monte Carlo iterations until you run out of time

        # And then pick best move

        self.prev = update
        self.root.printTree()
        return('pass!')
        
    # Given a gamestate and a following gamestate, find what move (if any)
    # was made by player color
    def findMoveMade(self, prev, update, color):

        # Determine which piece was played by comparing hands
        piecePlayed = None
        prevHand = prev.getHand(color)
        newHand = update.getHand(color)
        for piece in prevHand.keys():
            if prevHand[piece] != newHand[piece]:
                piecePlayed = piece
                break

        if piecePlayed == None:
            return "pass!"

        # Find coordinates that have changed
        size = Gamestate.referenceHand[piece].size
        coordinates = np.zeros((2, size), dtype = np.int)
        squaresFound = 0
        for i in range(0, Gamestate.boardsize):
            for j in range(0, Gamestate.boardsize):
                if prev.board[i,j] == 0 and update.board[i,j] == color:
                    coordinates[0, squaresFound] = j
                    coordinates[1, squaresFound] = i
                    squaresFound = squaresFound + 1
                    if squaresFound == size:
                        break
            if squaresFound == size:
                break

        orientation = Gamestate.referenceHand[piece].matchingOrientation(coordinates)
        moveExtremes = findExtremes(coordinates)
        minx, miny = moveExtremes[0], moveExtremes[2]

        return (piece, orientation, minx, miny)

            
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
