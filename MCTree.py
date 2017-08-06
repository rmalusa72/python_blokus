# MCTREE.PY
# Contains node for Monte Carlo search tree and related functions

from Gamestate import *
from Players import *
import sys
import random
import pdb

# Picks a random move from a list, but weights choice by size of each piece
def weightedRandomMove(moves):
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

    # Prints the tree rooted at this node
    def printTree(self):
        print("root")
        sys.stdout.write("Wins: ")
        sys.stdout.write(str(self.wins))
        sys.stdout.write("/Playouts:")
        print(str(self.playouts))
        self.printTreeRec(1)
        
    # Recursive helper method for printTree
    def printTreeRec(self, indent):
        for move, child in self.children.items():
            for i in range(0, indent):
                sys.stdout.write("\t")
            print(move)
            sys.stdout.write("Wins: ")
            sys.stdout.write(str(child.wins))
            sys.stdout.write("/Playouts:")
            print(str(child.playouts))
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
        sim_result = new_node.simulateGameWithFirstMoves()
        
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

    def simulateGameWithFirstMoves(self):
        
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
