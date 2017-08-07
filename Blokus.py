# BLOKUS.PY
# Main file containing setup and gameplay loop 

import sys
import numpy as np
import Pieces
import Players
import HumanPlayer
import MaxnPlayers
import MCTSPlayers
import Gamestate

# Initialize current gamestate variable
curr = Gamestate.Gamestate()
referenceHand = Gamestate.initHand() # for checks, etc.

# Fill list of players with humans and AIs, based on player input
players = dict()
for i in range(1,5):
    print("Is player %d AI or human?" % i)
    print("(0 for human, 1 for AI)")
    success = False

    while not success:
        try:
            n = int(raw_input())
            if n!=0 and n!= 1 and n!=2 and n!= 3 and n!= 4 and n!=5:
                print("Please enter zero or one only")
            else:
                success = True
        except ValueError as e:
            print("Please enter valid integers")

    if n == 0:
        players[i] = HumanPlayer.HumanPlayer(i)
    if n == 1:
        players[i] = Players.veryStupidAIPlayer(i)
    if n == 2:
        players[i] = MCTSPlayers.monteCarloPlayer(i)
    if n == 3:
        players[i] = MaxnPlayers.impracticallyThoroughAIPlayer(i)
    if n == 4:
        players[i] = MaxnPlayers.xPlyAIPlayer(i)
    if n == 5:
        players[i] = MCTSPlayers.persistentMCPlayer(i)

# MAIN GAME LOOP
# Quit when curr is terminal (aka four consecutive passes have occurred)
while not curr.isTerminal():

    curr.printBoard()
    # Repeat ask-for-move loop until valid move successfully acquired
    success = False
    while not success:
        # Ask for move
        move = players[curr.turn].getMove(curr.duplicate())
        # A pass is a single string ('pass!') and has len = 5; otherwise len = 4
        if len(move) != 4:
            print("Passing!")
            curr.update(move)
            success = True
        elif curr.update(move) != False:
            success = True
        else:
            print("Invalid move!") 

curr.printScores()

# Temporarily here - write monte carlo search tree from persistent player at game end
for i in range(1,5):
    if isinstance(players[i], MCTSPlayers.persistentMCPlayer):
        players[i].writeTree()
