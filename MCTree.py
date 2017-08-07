# MCTREE.PY
# Contains node for Monte Carlo search tree and related functions

from Gamestate import *
from Players import *
import sys
import random
import pdb

def weightedRandomMove(moves):
    """Return a random move from moves, weighted by piece size."""
    weightedlist = list()
    for move in moves:
        if move != 'pass!':
            for i in range(0, Gamestate.Gamestate.referenceHand[move[0]].size):
                weightedlist.append(move)
        else:
            weightedlist.append('pass!')
                
    return random.choice(weightedlist)


class MCNode():

    def __init__(self, gamestate, parent = None, fullyExpanded = False, playouts = 0):
        self.gamestate = gamestate
        self.parent = parent
        self.children = dict()
        self.fullyExpanded = False
        self.playouts = playouts
        self.wins = [0,0,0,0]
        
    def printTree(self):
        """Print the tree written on this node."""
        print("root")
        sys.stdout.write("Wins: ")
        sys.stdout.write(str(self.wins))
        sys.stdout.write("/Playouts:")
        print(str(self.playouts))
        self.printTreeRec(1)
        
    def printTreeRec(self, indent):
        """Recursive helper function for printTree."""
        for move, child in self.children.items():
            for i in range(0, indent):
                sys.stdout.write("\t")
            print(move)
            sys.stdout.write("Wins: ")
            sys.stdout.write(str(child.wins))
            sys.stdout.write("/Playouts:")
            print(str(child.playouts))
            child.printTreeRec(indent + 1)

    def updateStats(self, utility_vector):
        """Update node's wins and playouts based on a descendant's utility vector."""
        self.playouts = self.playouts + 1
        for i in range(0,4):
            if utility_vector[i] == 1:
                self.wins[i] = self.wins[i] + 1

    def expand(self):
        """Expand a random unvisited child from node, play out simulation, update stats, and return utility vector result."""
        if self.gamestate.isTerminal():
            utilityVector = utility(self.gamestate)
            self.updateStats(utilityVector)
            return utilityVector
        
        unexplored_moves = self.gamestate.listMoves()
        for move, child in self.children.items():
            try:
                unexplored_moves.remove(move)
            except ValueError:
                pdb.set_trace()
        print("Moves remaining:")
        print(unexplored_moves)
        print("Testing:")
        randMove = weightedRandomMove(unexplored_moves)
        print(randMove)
        
        # Expand
        new_gamestate = self.gamestate.duplicate()
        new_gamestate.update(randMove)
        self.children[randMove] = MCNode(new_gamestate, parent = self)
        new_node = self.children[randMove]
        
        # Run simulation from new node
        sim_result = new_node.simulateWeightedGame()
        
        # Update own stats with this result
        self.updateStats(sim_result)
        
        # Update fullyExpanded if necessary
        if len(unexplored_moves) == 1:
            self.fullyExpanded = True

        # Return result of simulation (utility vector) for backpropagation
        return sim_result

    def simulateGame(self):
        """Simulate a random game starting from this node, and return utility vector outcome."""

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

    def simulateWeightedGame(self):
        """Simulate a game with random moves weighted by piece size, and return utility vector outcome."""
        print("Simulating weighted random game..")

        # Simulate game 
        gamestate = self.gamestate.duplicate()
        while not gamestate.isTerminal():
            moves = gamestate.listMoves()
            randMove = weightedRandomMove(moves)
            gamestate.update(randMove)
            
        # Update playout and win count in self
        utility_vector = utility(gamestate)
        self.updateStats(utility_vector)

        # Return utility vector for backpropagation
        return utility_vector

    def simulateGameWithFirstMoves(self):
        """Simulate a game where players pick first moves, and return utility vector outcome."""
        print("Simulating game with first moves...")

        # Simulate game
        gamestate = self.gamestate.duplicate()
        while not gamestate.isTerminal():
            move = gamestate.canMove()
            if not move == False:
                gamestate.update(move)
            else:
                gamestate.update('pass!')

        # Update playout and win count in self
        utility_vector = utility(gamestate)
        self.updateStats(utility_vector)

        # Return utility vector for backpropagation
        return utility_vector
