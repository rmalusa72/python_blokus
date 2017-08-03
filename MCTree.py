# MCTREE.PY
# Contains node for Monte Carlo search tree and related functions

from Gamestate import *
from Players import *
import random
import pdb
    
class MCNode():

    def __init__(self, gamestate, parent = None, children = dict(), fullyExpanded = False, playouts = 0, wins = [0,0,0,0]):
        self.gamestate = gamestate
        self.parent = parent
        self.children = children
        self.fullyExpanded = False
        self.playouts = playouts
        self.wins = wins

    # Given a utility vector for a terminal gamestate descended from this node,
    # update wins and playouts accordingly
    def updateStats(self, utility_vector):
        print("Previous state of node:")
        print(self.wins)
        print(self.playouts)
        print("Updating stats of node")
        print(self)
        print("with vector")
        print(utility_vector)
        self.playouts = self.playouts + 1
        for i in range(0,4):
            if utility_vector[i] == 1:
                self.wins[i] = self.wins[i] + 1
        
    # Expands a random unvisited child from node, plays out simulation from it,
    # updates fullyExpanded to true if all children have been explored, and returns
    # results of simulation
    def expand(self):

        unexplored_moves = self.gamestate.listMoves()
        print("Unexplored moves:")
        print(unexplored_moves)
        for move, child in self.children.items():
            print("Removing tried move:")
            print(move)
            try:
                unexplored_moves.remove(move)
            except ValueError:
                pdb.set_trace()
        randMove = random.choice(unexplored_moves)
        print(randMove)
        
        # Expand
        new_gamestate = self.gamestate.duplicate()
        new_gamestate.update(randMove)
        self.children[randMove] = MCNode(new_gamestate, parent = self)
        new_node = self.children[randMove]
        
        # Run simulation from new node
        print("wins before simulation:")
        print(self.wins)
        sim_result = new_node.simulateGame()
        print("wins after simulation:")
        print(self.wins)
        
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
        # Simulate game 
        gamestate = self.gamestate.duplicate()
        while not gamestate.isTerminal():
            moves = gamestate.listMoves()
            randMove = random.choice(moves)
            print(randMove)
            gamestate.update(randMove)
            print(gamestate.board)
            
        # Update playout and win count in self
        utility_vector = utility(gamestate)
        self.updateStats(utility_vector)

        # Return utility vector for backpropagation
        return utility_vector
