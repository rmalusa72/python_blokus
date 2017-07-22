# GAMESTATE.PY
# Contains a class representing a specific state in the game space - turn, hands,
# board, etc. - and functions useful for setup of gamestates

from Pieces import *
import sys
import numpy as np

# Initializes a beginning hand with one of each piece
def initRefHand():
    rtn = dict()
    rtn['One'] = One()
    rtn['Two'] = Two()
    rtn['I3'] = I3()
    rtn['V3'] = V3()
    rtn['I4'] = I4()
    rtn['L4'] = L4()
    rtn['N4'] = N4()
    rtn['O'] = O()
    rtn['T4'] = T4()
    rtn['F'] = F()
    rtn['I'] = I()
    rtn['L'] = L()
    rtn['N'] = N()
    rtn['P'] = P()
    rtn['T'] = T()
    rtn['U'] = U()
    rtn['V'] = V()
    rtn['W'] = W()
    rtn['X'] = X()
    rtn['Y'] = Y()
    rtn['Z'] = Z()
    return rtn

def initHand():
    rtn = dict()
    rtn['One'] = True
    rtn['Two'] = True
    rtn['I3'] = True
    rtn['V3'] = True
    rtn['I4'] = True
    rtn['L4'] = True
    rtn['N4'] = True
    rtn['O'] = True
    rtn['T4'] = True
    rtn['F'] = True
    rtn['I'] = True
    rtn['L'] = True
    rtn['N'] = True
    rtn['P'] = True
    rtn['T'] = True
    rtn['U'] = True
    rtn['V'] = True
    rtn['W'] = True
    rtn['X'] = True
    rtn['Y'] = True
    rtn['Z'] = True
    return rtn

# Initializes a list with the starting corner for a given player
def startCorner(color, boardsize):
    corners = list()
    if color == 1:
        corners.append(np.array([[-1,0],[-1,0]]))
    if color == 2:
        corners.append(np.array([[-1,0],[boardsize, boardsize-1]]))
    if color == 3:
        corners.append(np.array([[boardsize, boardsize-1],
                                 [boardsize, boardsize-1]]))
    if color == 4:
        corners.append(np.array([[boardsize, boardsize-1],[-1,0]]))
    return corners

# Initializes an empty board of size boardSize
def initBoard(boardSize):
    board = np.zeros((boardSize,boardSize),dtype=int)
    return board

class Gamestate:
    '''Represents a game state in Blokus, with hands and board'''

    # NOTE: Change things to use single reference hand instead of each gamestate
    # having four, that is gonna be inefficient when going thru the probability
    # space
    referenceHand = initRefHand()
    
    # Makes a beginning game state
    def __init__(self, boardsize):
        self.blue = initHand()
        self.yellow = initHand()
        self.red = initHand()
        self.green = initHand()
        self.bcorners = startCorner(1, boardsize)
        self.ycorners = startCorner(2, boardsize)
        self.rcorners = startCorner(3, boardsize)
        self.gcorners = startCorner(4, boardsize)
        self.board = initBoard(boardsize)
        self.boardsize = boardsize
        self.turn = 1
        self.passCount = 0


    # Updates gamestate with provided move if it is legal,
    # or else returns False
    def update(self, move):

        if len(move) != 4: # Then move is a pass
            self.passCount = self.passCount + 1
            self.advanceTurn()
            return
        
        name = move[0]
        color = self.turn
        
        # If player doesn't have piece, move is illegal
        if not self.getHand(color)[name]:
            return False
        piece = Gamestate.referenceHand[name]

        # Set piece to correct orientation and location
        orientation = move[1]
        piece.setOrientation(orientation)

        move_xmin = move[2]
        move_ymin = move[3]
        piece_extremes = findExtremes(piece.shape)
        piece_xmin, piece_ymin = piece_extremes[0], piece_extremes[2]
        xdif = move_xmin - piece_xmin
        ydif = move_ymin - piece_ymin
        piece.translate(xdif, ydif)

        # Check if move is legal
        if not self.moveCheck(piece):
            return False

        # Set appropriate squares to player color
        self.colorSet(piece.shape, self.turn)

        # Update corner list
        self.updateCorners(self.turn, piece.corners)
        print("Updated corners:")
        print(self.getCorners(self.turn))

        # Remove piece played from hand
        self.getHand(self.turn)[name] = False

        # Reset pass count
        self.passCount = 0
        
        # Advance turn
        self.advanceTurn()
    
        
    # Returns whether a move (as oriented and located piece) is valid
    def moveCheck(self, piece):
        
        # Check if one of piece's corners matches an open corner on the board
        # NOTE: make function to break 2x2n corners array into list of individual
        # corners, I do it several times
        bcorners = self.getCorners(self.turn)
        pcorners = piece.corners
        diagonal = False
        for cur in splitCornerArray(pcorners):
            inv = np.array([[cur[0,1],cur[0,0]],[cur[1,1],cur[1,0]]])
            for j in range(0, len(bcorners)):
                if np.array_equal(bcorners[j],inv):
                    diagonal = True
                    break
            if diagonal:
                break

        if not diagonal:
            return False

        # Make sure piece does not conflict with anything already on
        # the board
        if not self.moveConflicts(piece):
            return True
        return False

    # Checks whether a piece conflicts (overlaps or edge adacent with)
    # anything already on board
    def moveConflicts(self, p):

        color = self.turn
        
        # This dict with string keys will have values that are either
        # 2x1 arrays (for points to check, surrounding each tile in proposed
        # move) or False (if the points are off the board or also in the
        # proposed move)
        nears = dict()

        # Iterate through each tile in the proposed move
        for i in range(0, p.size):
            
            x = p.shape[0,i]
            y = p.shape[1,i]

            # If point is off board, conflict
            if x < 0 or y < 0 or x >= self.boardsize or y >= self.boardsize:
                return True

            # If tile is already occupied, there is a conflict
            if self.board[y,x] != 0:
                return True

            # Reset coordinates
            nears['e'] = False
            nears['s'] = False
            nears['w'] = False
            nears['n'] = False

            # Change 'nears' to appropriate coordinates where they exist
            if x < (self.boardsize - 1):
                nears['e'] = np.array([[x+1],[y]])

            if y < (self.boardsize - 1):
                nears['s'] = np.array([[x],[y+1]])

            if x > 0:
                nears['w'] = np.array([[x-1],[y]])

            if y > 0:
                nears['n'] = np.array([[x],[y-1]])

            # Disregard coordinates that are in the move itself
            for dir, coord in nears.items():
                if coord is not False:
                    for j in range(0, p.size):
                        if np.array_equal(coord,p.shape[:,j].reshape(2,1)):
                            coord = False

            # If any laterally adjacent tiles are player color, move is invalid
            for dir in ['e', 's', 'n', 'w']:
                if nears[dir] is not False:
                    if self.board[nears[dir][1,0]][nears[dir][0,0]] == color: 
                        return True

        return False
        
    # Update turn to next player
    def advanceTurn(self):
        self.turn = self.turn + 1
        if self.turn == 5:
            self.turn = 1

    # Returns the hand corresponding to int color    
    def getHand(self, color):
        if color == 1:
            return self.blue
        if color == 2:
            return self.yellow
        if color == 3:
            return self.red
        if color == 4:
            return self.green

    # Returns a hand as a list sorted by piece size
    def sortedHand(self, color):
        rtn = list()
        hand = self.getHand(color)
        sortednames = ["F","I","L","N","P","T","U","V","W","X","Y","Z",
                       "I4", "L4", "N4", "O", "T4",
                       "I3","V3",
                       "Two",
                       "One"]
        for name in sortednames:
            if hand[name]:
                rtn.append(Gamestate.referenceHand[name])
        return rtn

    # Returns the corner list corresponding to int color
    def getCorners(self, color):
        if color == 1:
            return self.bcorners
        if color == 2:
            return self.ycorners
        if color == 3:
            return self.rcorners
        if color == 4:
            return self.gcorners

    # Given a 2x2n matrix of corners, update appropriate color's corner list
    def updateCorners(self, color, corners):
        oldList = self.getCorners(color)
        for cur in splitCornerArray(corners):
            inv = np.array([[cur[0,1],cur[0,0]],[cur[1,1],cur[1,0]]])
            obliterated = False
            for j in range(0, len(oldList)):
                if np.array_equal(oldList[j],inv):
                    del oldList[j]
                    obliterated = True
                    break
            if -1 in cur or self.boardsize in cur:
                continue
            if not obliterated:
                oldList.append(cur)

    # Given a 2xn matrix of coordinates, set those to int color
    def colorSet(self, coords, color):
        if not (color in range(1,5)):
            return False
        for i in range(coords[0].size):
            if self.board[coords[1,i]][coords[0,i]] != 0:
                return False
            self.board[coords[1,i]][coords[0,i]] = color
        return True

    # Returns list of possible moves for current player
    def listMoves(self):
        rtn = list()

        hand = self.getHand(self.turn)
        corners = self.getCorners(self.turn)

        # If no corners or no pieces in hand, no moves are possible
        if not (True in hand.values()) or len(corners) == 0:
            return rtn

        # For each piece, find list of moves for each orientation
        # with findPieceMoves
        sortedHand = self.sortedHand(self.turn)
        for piece in sortedHand:
            rtn.extend(self.findPieceMoves(piece))

            if piece.r90 and piece.r180:
                for i in range(3):
                    piece.rotate(1)
                    rtn.extend(self.findPieceMoves(piece))
            elif piece.r90 and not piece.r180:
                piece.rotate(1)
                rtn.extend(self.findPieceMoves(piece))
                
            if piece.chiral:
                piece.flipV()
                rtn.extend(self.findPieceMoves(piece))

                if piece.r90 and piece.r180:
                    for i in range(3):
                        piece.rotate(1)
                        rtn.extend(self.findPieceMoves(piece))
                elif piece.r90 and not piece.r180:
                    piece.rotate(1)
                    rtn.extend(self.findPieceMoves(piece))
        return rtn

    # Find all moves for a given piece in a specific orientation
    def findPieceMoves(self, p):

        rtn = list()
        bcorners = self.getCorners(self.turn)
        piece_extremes = findExtremes(p.shape)
        piece_xmin, piece_ymin = piece_extremes[0], piece_extremes[2]
        
        # For each corner pc on the piece...
        pcorners = p.corners
        for pc in splitCornerArray(pcorners):

            # For each corner bc on the board...
            for bc in bcorners:

                inv = np.array([[bc[0,1],bc[0,0]],[bc[1,1],bc[1,0]]])
                
                # Check if orientation of pc matches flipped bc:
                if ((pc[0,1] - pc[0,0]) == (inv[0,1] - inv[0,0]) and
                    (pc[1,1] - pc[1,0]) == (inv[1,1] - inv[1,0])):

                    # Move piece to matching location
                    xdif = inv[0,0] - pc[0,0]
                    ydif = inv[1,0] - pc[1,0]
                    p.translate(xdif, ydif)
                    piece_xmin += xdif
                    piece_ymin += ydif
                    
                    # Now check if move is appropriate
                    if not self.moveConflicts(p):
                        rtn.append((p.name, p.orientation, piece_xmin, piece_ymin))

        return rtn


    # Like listMoves, but returns true as soon as it finds a single move
    def canMove(self):
        hand = self.getHand(self.turn)
        corners = self.getCorners(self.turn)

        # If no corners or no pieces in hand, no moves are possible
        if not (True in hand.values()) or len(corners) == 0:
            return False

        # For each piece, find list of moves for each orientation
        # with findPieceMoves
        sortedHand = self.sortedHand(self.turn)
        for piece in sortedHand:
            if self.canFindPieceMoves(piece):
                return True

            if piece.r90 and piece.r180:
                for i in range(3):
                    piece.rotate(1)
                    if self.canFindPieceMoves(piece):
                        return True                    
            elif piece.r90 and not piece.r180:
                piece.rotate(1)
                if self.canFindPieceMoves(piece):
                    return True
                
            if piece.chiral:
                piece.flipV()
                if self.canFindPieceMoves(piece):
                    return True
                if piece.r90 and piece.r180:
                    for i in range(3):
                        piece.rotate(1)
                        if self.canFindPieceMoves(piece):
                            return True
                elif piece.r90 and not piece.r180:
                    piece.rotate(1)
                    if self.canFindPieceMoves(piece):
                        return True
        return False

    # canMove's equivalent of findPieceMoves (returns True as soon as it
    # finds a single move)
    def canFindPieceMoves(self, p):

        bcorners = self.getCorners(self.turn)
        piece_extremes = findExtremes(p.shape)
        piece_xmin, piece_ymin = piece_extremes[0], piece_extremes[2]
        
        # For each corner pc on the piece...
        pcorners = p.corners
        for pc in splitCornerArray(pcorners):

            # For each corner bc on the board...
            for bc in bcorners:

                inv = np.array([[bc[0,1],bc[0,0]],[bc[1,1],bc[1,0]]])
                
                # Check if orientation of pc matches flipped bc:
                if ((pc[0,1] - pc[0,0]) == (inv[0,1] - inv[0,0]) and
                    (pc[1,1] - pc[1,0]) == (inv[1,1] - inv[1,0])):

                    # Move piece to matching location
                    xdif = inv[0,0] - pc[0,0]
                    ydif = inv[1,0] - pc[1,0]
                    p.translate(xdif, ydif)
                    piece_xmin += xdif
                    piece_ymin += ydif
                    
                    # Now check if move is appropriate
                    if not self.moveConflicts(p):
                        return True

        return False

    # Returns true if gamestate is terminal (four consecutive passes), otherwise
    # returns false
    def isTerminal(self):
        if self.passCount >= 4:
            return True
        return False
    
    # Print current scores
    def printScores(self):
        scores = [0,0,0,0]
        for i in range(1, 5):
            hand = self.getHand(i)
            for name, val in hand.items():
                if val:
                    scores[i-1] = scores[i-1] - Gamestate.referenceHand[name].size

        print("Final scores:")
        print("Blue:")
        print scores[0]
        print("Yellow:")
        print scores[1]
        print("Red:")
        print scores[2]
        print("Green:")
        print scores[3]
    
    # Print board
    def printBoard(self):
        print self.board
        
    # Print a player's hand
    def printHand(self, i):
        hand = self.getHand(i)
        for name, val in hand.items():
            if val:
                sys.stdout.write(name + ' ')
        sys.stdout.write("\n")

    # Print a player's hand sorted by piece size
    def printSortedHand(self, i):
        sortedhand = self.sortedHand(i)
        for p in sortedhand:
            sys.stdout.write(p.name + ' ')
        sys.stdout.write("\n")
    
    # Copy this gamestate
    #def copy(self):
        # IMPLEMENT THIS
