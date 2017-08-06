# MCTSPLAYERS.PY
# Contains player using Monte Carlo Tree Search and its functions

import Pieces
import Gamestate
import Players
import MCTree
import numpy as np
import time
    
class monteCarloPlayer(Players.AIPlayer):
    def getMove(self, update):
        
        # If this is the first time getMove is called,
        # initialize 'root' and 'current' to node w/ opening gamestate
        if not hasattr(self, 'root'):
            self.root = MCTree.MCNode(Gamestate.Gamestate())
            self.current = self.root

        # Determine which moves have been made by each player in order to
        # move 'current' down the tree to the node corresponding to update
        if not self.current is self.root:
            colorToCheck = self.color + 1
            if colorToCheck == 5:
                colorToCheck = 1
            while True:

                # Find move made by player, then move down tree to corresponding
                # node, or create it if necessary
                moveMade = self.findMoveMade(self.current.gamestate, update, colorToCheck)

                if moveMade in self.current.children:
                    self.current = self.current.children[moveMade]
                else:
                    new_gamestate = self.current.gamestate.duplicate()
                    new_gamestate.update(moveMade)
                    self.current.children[moveMade] = MCTree.MCNode(new_gamestate, parent = self.current)
                    self.current = self.current.children[moveMade]

                # Go to next player in order
                colorToCheck = colorToCheck + 1
                if colorToCheck == 5:
                    colorToCheck = 1
                if colorToCheck == self.color:
                    break
                
        # Then repeat Monte Carlo iterations until you run out of time

        start_time = time.time()
        while (time.time() - start_time < 30):
            self.mcIteration()

        self.current.printTree()
        
        # And pick best move

        move = self.highestAvgPlayoutMove(self.current)

        # Update tree to reflect path taken
        if move in self.current.children:
            self.current = self.current.children[move]
        else:
            new_gamestate = self.current.duplicate()
            new_gamestate.update(move)
            self.current.children[move] = MCNode(new_gamestate, parent = self.current)
            self.current = self.current.children[move]

        # Then return the move to make
        print("MAKING MOVE:")
        print(move)
        print("self.current.gamestate.board:")
        print(self.current.gamestate.board)
        return(move)
        
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
        size = Gamestate.Gamestate.referenceHand[piece].size
        coordinates = np.zeros((2, size), dtype = np.int)
        squaresFound = 0
        for i in range(0, Gamestate.Gamestate.boardsize):
            for j in range(0, Gamestate.Gamestate.boardsize):
                if prev.board[i,j] == 0 and update.board[i,j] == color:
                    coordinates[0, squaresFound] = j
                    coordinates[1, squaresFound] = i
                    squaresFound = squaresFound + 1
                    if squaresFound == size:
                        break
            if squaresFound == size:
                break

        orientation = Gamestate.Gamestate.referenceHand[piece].matchingOrientation(coordinates)
        moveExtremes = Pieces.findExtremes(coordinates)
        minx, miny = moveExtremes[0], moveExtremes[2]

        return (piece, orientation, minx, miny)

            
    # A single runthrough/expansion/playout of the Monte Carlo search tree
    def mcIteration(self):

        # Step through the tree according to upper confidence bounds until we
        # reach a node whose children have not all been explored
        node = self.current
        canStep = self.ucbStep(node)
        while not canStep == False:
            node = node.children[canStep]
            canStep = self.ucbStep(node)

        # Then expand that node, saving the result (utility vector) of
        # random playout
        result = node.expand()

        # Backpropagate that result through node's parents
        while not node is self.current:
            node = node.parent
            node.updateStats(result)

    # Given an MCNode, returns the move corresponding to its child with the highest
    # average playout
    def highestAvgPlayoutMove(self, node):
        color = node.gamestate.turn
        highestAvg = -1
        highestAvgMove = None
        for move, child in node.children.items():
            currNodeAvg = child.wins[color-1]/(child.playouts*1.0)
            if currNodeAvg > highestAvg:
                highestAvg = currNodeAvg
                highestAvgMove = move
        return highestAvgMove
            
    # Given an MCNode, returns the move corresponding to its child with the highest
    # upper confidence bound (for the player at that node)
    def highestUCBMove(self, node):
        color = node.gamestate.turn
        highestUCB = -1
        highestUCBMove = None
        for move, child in node.children.items():
            
            # The upper confidence bound of a node is
            # xi + sqrt(2*ln(n)/ni)
            # where n is total playouts from current gamestate,
            # ni = total playouts from node i,
            # wi = total wins from node i for player color, 
            # and xi = average payout for node i (wi/ni)
            currNodeUCB = (child.wins[color-1]/(child.playouts*1.0)
                           + np.sqrt(2 * np.log(self.current.playouts)
                                     / (child.playouts * 1.0)))
            if currNodeUCB > highestUCB:
                highestUCB = currNodeUCB
                highestUCBMove = move
        return highestUCBMove
            
    # Given an MCNode, returns the move corresponding to the child with the highest
    # upper confidence bound (for the player at that node)
    # if all children have been explored, or false otherwise
    def ucbStep(self, node):
        if node.fullyExpanded:
            return self.highestUCBMove(node)
        else:
            return False
