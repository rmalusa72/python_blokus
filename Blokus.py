# BLOKUS.PY
# Main file containing setup and gameplay loop 

import sys
import numpy as np
from Pieces import *
from Gamestate import *
from Players import *

# Initialize current gamestate variable
curr = Gamestate(20)
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
            if n!=0 and n!= 1:
                print("Please enter zero or one only")
            else:
                success = True
        except ValueError as e:
            print("Please enter valid integers")

    if n == 0:
        players[i] = HumanPlayer(i)
    if n == 1:
        players[i] = AIPlayer(i)

# MAIN GAME LOOP
# Quit when passCount reaches four consecutive passes
passCount = 0 
while passCount != 4:
    movelist = curr.listMoves()
    print(movelist)
    if len(movelist) != 0:
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
                passCount = passCount + 1
            elif curr.update(move) != False:
                success = True
                passCount = 0
            else:
                print("Invalid move!") 
    else:
        print("Player has no moves - passing")
        passCount = passCount + 1

