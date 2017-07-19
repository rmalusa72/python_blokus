import sys
import numpy as np
from Pieces import *
from Gamestate import *
from Players import *

# Main file containing setup and main game loop 
            
# Function to check if a move is legal (move is a list where first item is name and
# rest of list is coordinate tuples)
def moveCheck(move, color):

    name = move[0]

    # If player doesn't have piece, move is illegal
    if not name in curr.getHand(color):
        return False

    # Move is now the nparray of coordinates
    move = move[1]
    
    # If the # of tuples is not the same as the size of the piece, move is illegal
    if not move[0].size == curr.getHand(color)[name].size:
        return False
    
    shape = toBoolArray(move)

    # Compare shape of coordinate tuples in move to the piece they claim to be
    if not curr.getHand(color)[name].isThisPiece(shape):
        return False

    # Now we know the piece is the right size, shape, & possessed by the player,
    # and can check if the actual move is valid.
    
    # This dict with string keys and bool values will contain either 2x1 arrays
    # (for points to check, surrounding each tile in proposed move) or False
    # (if the points are off the board or also in the proposed move)
    nears = dict()

    # whether we have found a successful diagonal connection
    diagonal = False

    boardsize = curr.board[0].size

    # Now iterate through each tile in the proposed move
    for i in range(0, move[0].size):

        x = move[0,i]
        y = move[1,i]

        # Reset coordinates (only update diagonals if we don't
        # have one yet)
        nears['e'] = False
        nears['s'] = False
        nears['w'] = False
        nears['n'] = False

        if not diagonal: 
            nears['ne'] = False
            nears['nw'] = False
            nears['se'] = False
            nears['sw'] = False

        # Now change 'nears' to appropriate coordinates where they exist
        if x < (boardsize - 1):
            nears['e'] = np.array([[x+1],[y]])
            if y > 0 and not diagonal:
                nears['ne'] = np.array([[x+1],[y-1]])
            if y < (boardsize - 1) and not diagonal:
                nears['se'] = np.array([[x+1],[y+1]])

        if y < (boardsize - 1):
            nears['s'] = np.array([[x],[y+1]])

        if x > 0:
            nears['w'] = np.array([[x-1],[y]])
            if y > 0 and not diagonal:
                nears['nw'] = np.array([[x-1],[y-1]])
            if y < (boardsize-1) and not diagonal:
                nears['sw'] = np.array([[x-1], [y+1]])

        if y > 0:
            nears['n'] = np.array([[x],[y-1]])

        # Disregard coordinates that are in the set of tiles in the move itself
        for dir, coord in nears.items():
            if coord is not False:
                for j in range(0, move[0].size):
                    if np.array_equal(coord,move[:,j].reshape(2,1)):
                        coord = False

        # If any laterally adjacent tiles are player color, move is invalid
        for dir in ['e', 's', 'n', 'w']:
            if nears[dir] is not False:
                if curr.board[nears[dir][1,0]][nears[dir][0,0]] == color: 
                    return False

        # If any diagonally adjacent tiles are player color, set diagonal to true
        for dir in ['ne','nw','se','sw']:
            if nears[dir] is not False:
                if curr.board[nears[dir][1,0]][nears[dir][0,0]] == color:
                    diagonal = True

    # If this is the first piece the player places, they don't need a diagonal
    # connection, but do need it to touch a corner
    if len(curr.getHand(color)) == 21:
        if color == 1:
            corner = np.array([[0],[0]])
        if color == 2:
            corner = np.array([[0],[boardsize-1]])
        if color == 3:
            corner = np.array([[boardsize-1],[boardsize-1]])
        if color == 4:
            corner = np.array([[boardsize-1],[0]])
        for i in range(0, move[0].size):
            if np.array_equal(corner, move[:,i].reshape(2,1)):
                diagonal = True
            
    return diagonal


# MAIN GAME CODE STARTS HERE

# Initialize current gamestate variable
curr = Gamestate(20)
referenceHand = initHand() # Reference hand with all pieces, for checks/etc

# Fill list of players with humans and AIs, based on player input
players = dict()
for i in range(1,5):
    print("Is player %d AI or human?" % i)
    print("(0 for human, 1 for AI)")
    n = int(raw_input())
    if n == 0:
        players[i] = HumanPlayer(i)
    if n == 1:
        players[i] = AIPlayer(i)

# MAIN GAME LOOP
passCount = 0 # Number of consecutive passes; quit when this reaches 4
while passCount != 4:
    if curr.canMove(curr.turn):
        success = False # Whether an acceptable move has been made
        while not success:
        # Get move in form of list of tuples - first is piece name, then coords
            move = players[curr.turn].getMove(curr)
            if len(move) != 2:       # Valid move is 2 items long; less than that is a pass
                passCount = passCount + 1
                success = True
            elif moveCheck(move, curr.turn): # Otherwise check move and set
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

                # Now piece.corners has actual corners!!! Update corner list
                curr.updateCorners(curr.turn, piece.corners)

                del curr.getHand(curr.turn)[move[0]]
                success = True
                passCount = 0
            else:
                print("Invalid move!") # If moveCheck fails, prompt for another move
    else:
        print("Player has no moves - passing")
        passCount = passCount + 1

    curr.advanceTurn()

