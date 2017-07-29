# BLOKUS.PY
# Main file containing setup and gameplay loop 

import sys
import numpy as np
from Pieces import *
from Gamestate import *
from Players import *

# Initialize current gamestate variable
curr = Gamestate()
referenceHand = initHand() # for checks, etc.

# Fill list of players with humans and AIs, based on player input
players = dict()
for i in range(1,5):
    print("Is player %d AI or human?" % i)
    print("(0 for human, 1 for AI)")
    success = False

    while not success:
        try:
            n = int(raw_input())
            if n!=0 and n!= 1 and n!=2:
                print("Please enter zero or one only")
            else:
                success = True
        except ValueError as e:
            print("Please enter valid integers")

    if n == 0:
        players[i] = HumanPlayer(i)
    if n == 1:
        players[i] = veryStupidAIPlayer(i)
    if n == 2:
        players[i] = xPlyAIPlayer(i)

# MAIN GAME LOOP
# Quit when curr is terminal (aka four consecutive passes have occurred)
while not curr.isTerminal():

    curr.printBoard()
    if curr.canMove():
        # Repeat ask-for-move loop until valid move successfully acquired
        success = False
        while not success:
            # Ask for move
            move = players[curr.turn].getMove(curr)
            # A pass is an empty list and has len = 0; otherwise len = 4
            if len(move) != 4:
                print("Passing!")
                curr.update(move)
                success = True
            elif curr.update(move) != False:
                success = True
            else:
                print("Invalid move!") 
    else:
        print("Player has no moves - passing")
        curr.update(list())

curr.printScores()
