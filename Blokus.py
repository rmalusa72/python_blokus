import sys
import numpy as np
from Pieces import *
from Gamestate import *
from Players import *

# Main file containing setup and main game loop 

# MAIN GAME CODE STARTS HERE

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
    if curr.canMove(curr.turn):
        # Repeat ask-for-move loop until valid move successfully acquired
        success = False
        while not success:
            # Ask for move
            move = players[curr.turn].getMove(curr)
            # A pass is an empty list and has len = 0; otherwise len = 2
            if len(move) != 2: 
                passCount = passCount + 1
                success = True
            elif curr.moveCheck(move, curr.turn):
                # Set appropriate squares to player color
                curr.colorSet(move[1], curr.turn)

                # Get appropriate piece from hand 
                piece = curr.getHand(curr.turn)[move[0]]

                # Find min x, min y from move coords and move
                # piece to match move's location (movecheck set right orientation)
                # NOTE: getting min x, min y this many times is inefficient!
                # fix later
                move_extremes = findExtremes(move[1])
                move_xmin, move_ymin = move_extremes[0], move_extremes[2]
                piece_extremes = findExtremes(piece.shape)
                piece_xmin, piece_ymin = piece_extremes[0],piece_extremes[2]
                xdif = move_xmin - piece_xmin
                ydif = move_ymin - piece_ymin
                piece.translate(xdif, ydif)

                # Now piece.corners has correct corners, so update corner list
                curr.updateCorners(curr.turn, piece.corners)

                # Remove piece played from hand
                del curr.getHand(curr.turn)[move[0]]
                
                success = True
                passCount = 0
            else:
                print("Invalid move!") 
    else:
        print("Player has no moves - passing")
        passCount = passCount + 1

    curr.advanceTurn()

