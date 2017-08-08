# MCTSPLAYERS.PY
# Contains player using Monte Carlo Tree Search and its functions

import Pieces
import Gamestate
import Players
import MCTree
import BlokusFunctions as bfn
import numpy as np
import time
import cPickle as pickle
    
class monteCarloPlayer(Players.AIPlayer):
    def getMove(self, update):
        """Prompted with gamestate, return move chosen by monte carlo search tree."""
        
        # If this is the first time getMove is called,
        # initialize 'root' and 'current' to node w/ opening gamestate
        if not hasattr(self, 'root'):
            self.root = MCTree.MCNode(Gamestate.Gamestate())
            self.current = self.root

        # Determine which moves have been made by each player in order to
        # move 'current' down the tree to the node corresponding to update
        if not self.current.gamestate.equals(update):
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
        
    def findMoveMade(self, prev, update, color):
        """Return what move (if any) was made by provided player between prev and update.""" 

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
        moveExtremes = bfn.findExtremes(coordinates)
        minx, miny = moveExtremes[0], moveExtremes[2]

        return (piece, orientation, minx, miny)

    def mcIteration(self):
        """Iterate Monte Carlo search tree algorithm by doing a single step-through/expansion/playout/update."""

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
        node = node.parent
        while not node is None and not node is self.current:
            node.updateStats(result)
            node = node.parent

    def highestAvgPlayoutMove(self, node):
        """Return the move corresponding to the child of the given node with highest average playout."""
        color = node.gamestate.turn
        highestAvg = -1
        highestAvgMove = None
        for move, child in node.children.items():
            if child.playouts != 0:
                currNodeAvg = child.wins[color-1]/(child.playouts*1.0)
            else:
                currNodeAvg = 0
            if currNodeAvg > highestAvg:
                highestAvg = currNodeAvg
                highestAvgMove = move
        return highestAvgMove
            
    def highestUCBMove(self, node):
        """Return the move corresponding to the child of the given node with the highest UCB."""
        color = node.gamestate.turn
        highestUCB = -1
        highestUCBMove = None
        for move, child in node.children.items():
            if child.playouts != 0:
                # The upper confidence bound of a node is
                # xi + sqrt(2*ln(n)/ni)
                # where n is total playouts from current gamestate,
                # ni = total playouts from node i,
                # wi = total wins from node i for player color, 
                # and xi = average payout for node i (wi/ni)
                currNodeUCB = (child.wins[color-1]/(child.playouts*1.0)
                               + np.sqrt(2 * np.log(self.current.playouts)
                                         / (child.playouts * 1.0)))
            else:
                currNodeUCB = 0
            if currNodeUCB > highestUCB:
                highestUCB = currNodeUCB
                highestUCBMove = move
        return highestUCBMove
            
    def ucbStep(self, node):
        """If node is fully expanded, return move corresponding to child with highest UCB, else return false."""
        if node.fullyExpanded:
            return self.highestUCBMove(node)
        else:
            return False

class persistentMCPlayer(monteCarloPlayer):

    shouldReadTree = False
    
    def getMove(self, update):
        """Prompted with gamestate, return move chosen by MCTS with tree loaded from file."""

        # If this is the first time getMove is called, either read root from file
        # or initialize new one. Then set 'current' to last known gamestate
        if not hasattr(self, 'root'):
            if persistentMCPlayer.shouldReadTree:
                self.root = self.readTree()
            else:
                self.root = MCTree.MCNode(Gamestate.Gamestate())
            self.current = self.root

        # Determine which moves have been made by each player in order to
        # move 'current' down the tree to the node corresponding to update
        if not self.current.gamestate.equals(update):
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

    def writeTree(self):
        """Write MC tree to file."""
        file = open("treestorage","wb")
        pickle.dump(self.root, file, -1)
        file.close()

    def readTree(self):
        """Read MC tree from file."""
        file = open("treestorage","r")
        return pickle.load(file)
