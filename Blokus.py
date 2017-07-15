import sys
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

    # If the # of tuples is not the same as the size of the piece, move is illegal
    if not (len(move) - 1) == referenceHand[name].size:
        return False

    # Find min and max x and y
    xmin = move[1][0]
    ymin = move[1][1]
    xmax = move[1][0]
    ymax = move[1][1]

    for i in range(1, len(move)):
        curx = move[i][0]
        cury = move[i][1]
        if curx < xmin:
            xmin = curx
        if curx > xmax:
            xmax = curx
        if cury < ymin:
            ymin = cury
        if cury > ymax:
            ymax = cury

    # Find width and height
    width = xmax - xmin + 1
    height = ymax - ymin + 1

    # Make 'blank' 2d boolean list (all false) of correct size
    shape = list()
    for i in range(0, width):
        shape.append(list())
        for j in range(0, height):
            shape[i].append(False)

    # Switch appropriate coords to True 
    for i in range(1,len(move)):
        shape[move[i][0] - xmin][move[i][1] - ymin] = True

    # Compare shape of coordinate tuples in move to the piece they claim to be
    if not referenceHand[name].isThisPiece(shape):
        return False

    # Now we know the piece is the right size, shape, & possessed by the player,
    # and can check if the actual move is valid.
    
    # This dict with string keys and bool values will contain either tuples
    # (for points to check, surrounding each tile in proposed move) or False
    # (if the points are off the board or also in the proposed move)
    nears = dict()

    # whether we have found a successful diagonal connection
    diagonal = False

    boardsize = len(curr.board)

    # Now iterate through each tile in the proposed move
    for i in range(1, len(move)):

        x = move[i][0]
        y = move[i][1]

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
            nears['e'] = (x+1, y)
            if y > 0 and not diagonal:
                nears['ne'] = (x+1, y-1)
            if y < (boardsize - 1) and not diagonal:
                nears['se'] = (x+1, y+1)

        if y < (boardsize - 1):
            nears['s'] = (x, y+1)

        if x > 0:
            nears['w'] = (x-1, y)
            if y > 0 and not diagonal:
                nears['nw'] = (x-1, y-1)
            if y < (boardsize-1) and not diagonal:
                nears['sw'] = (x-1, y+1)

        if y > 0:
            nears['n'] = (x, y-1)

        # Disregard coordinates that are in the set of tiles in the move itself
        for dir, coord in nears.items():
            if coord is not False and coord in move[1:]:
                coord = False

        # If any laterally adjacent tiles are player color, move is invalid
        for dir in ['e', 's', 'n', 'w']:
            if nears[dir] is not False:
                if curr.board[nears[dir][0]][nears[dir][1]] == color: 
                    return False

        # If any diagonally adjacent tiles are player color, set diagonal to true
        for dir in ['ne','nw','se','sw']:
            if nears[dir] is not False:
                if curr.board[nears[dir][0]][nears[dir][1]] == color:
                    diagonal = True

    # If this is the first piece the player places, they don't need a diagonal
    # connection, but do need it to touch a corner
    if len(curr.getHand(color)) == 21:
        if color == 1:
            corner = (0,0)
        if color == 2:
            corner = (boardsize - 1,0)
        if color == 3:
            corner = (boardsize - 1, boardsize - 1)
        if color == 4:
            corner = (0, boardsize - 1)
        if corner in move[1:]:
            diagonal = True
            
    return diagonal


# MAIN GAME CODE STARTS HERE

# Initialize current gamestate variable
curr = Gamestate()
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
    for i in range(1,5):
        if curr.canMove(i):
            success = False # Whether an acceptable move has been made
            while not success:
            # Get move in form of list of tuples - first is piece name, then coords
                move = players[i].getMove(curr)
                if len(move) <= 1:       # Valid move is >=2 items long; less than that is a pass
                    passCount = passCount + 1
                    success = True
                elif moveCheck(move, i): # Otherwise check move and set
                    curr.colorSet(move[1:], i)
                    del curr.getHand(i)[move[0]]
                    success = True
                    passCount = 0
                else:
                    print("Invalid move!") # If moveCheck fails, prompt for another move
        else:
            print("Player has no moves - passing")
            passCount = passCount + 1



