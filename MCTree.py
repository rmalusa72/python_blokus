# MCTREE.PY
# Contains node for Monte Carlo search tree and related functions

from Gamestate import *
from Players import *
import sys
import random
import pdb
    
class MCNode():

    def __init__(self, gamestate, parent = None, fullyExpanded = False, playouts = 0):
        self.gamestate = gamestate
        self.parent = parent
        self.children = dict()
        self.fullyExpanded = False
        self.playouts = playouts
        self.wins = [0,0,0,0]

    # Prints the tree rooted at this node
    def printTree(self):
        print("root")
        print(self.gamestate.board)
        self.printTreeRec(1)
        
    # Recursive helper method for printTree
    def printTreeRec(self, indent):
        for move, child in self.children.items():
            for i in range(0, indent):
                sys.stdout.write("\t")
            print(move)
            print(child.gamestate.board)
            child.printTreeRec(indent + 1)

    # Given a utility vector for a terminal gamestate descended from this node,
    # update wins and playouts accordingly
    def updateStats(self, utility_vector):
        self.playouts = self.playouts + 1
        for i in range(0,4):
            if utility_vector[i] == 1:
                self.wins[i] = self.wins[i] + 1
        
    # Expands a random unvisited child from node, plays out simulation from it,
    # updates fullyExpanded to true if all children have been explored, and returns
    # results of simulation
    def expand(self):
        
        unexplored_moves = self.gamestate.listMoves()
        for move, child in self.children.items():
            try:
                unexplored_moves.remove(move)
            except ValueError:
                pdb.set_trace()
        randMove = random.choice(unexplored_moves)
        print(randMove)

        print("expanding")
        print(self.gamestate.board)
        print("picking from")
        print(unexplored_moves)
        
        # Expand
        new_gamestate = self.gamestate.duplicate()
        new_gamestate.update(randMove)
        self.children[randMove] = MCNode(new_gamestate, parent = self)
        new_node = self.children[randMove]
        
        # Run simulation from new node
        sim_result = new_node.simulateGame()
        
        # Update own stats with this result
        self.updateStats(sim_result)
        
        # Update fullyExpanded if necessary
        if len(unexplored_moves) == 1:
            self.fullyExpanded = True

        # Return result of simulation (utility vector) for backpropagation
        return sim_result

    # Simulates a random game starting from self's gamestate, and returns
    # the outcome as a vector of utility
    def simulateGame(self):

        print("Simulating random game..")

        # Simulate game 
        gamestate = self.gamestate.duplicate()
        while not gamestate.isTerminal():
            moves = gamestate.listMoves()
            randMove = random.choice(moves)
            gamestate.update(randMove)
            
        # Update playout and win count in self
        utility_vector = utility(gamestate)
        self.updateStats(utility_vector)

        # Return utility vector for backpropagation
        return utility_vector
