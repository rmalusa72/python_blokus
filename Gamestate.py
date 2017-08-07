# GAMESTATE.PY
# Contains a class representing a specific state in the game space - turn, hands,
# board, etc. - and functions useful for setup of gamestates

from copy import deepcopy
import Pieces
import sys
import numpy as np

def initRefHand():
    """Return a reference hand with one of each piece."""
    rtn = dict()
    rtn['One'] = Pieces.One()
    rtn['Two'] = Pieces.Two()
    rtn['I3'] = Pieces.I3()
    rtn['V3'] = Pieces.V3()
    rtn['I4'] = Pieces.I4()
    rtn['L4'] = Pieces.L4()
    rtn['N4'] = Pieces.N4()
    rtn['O'] = Pieces.O()
    rtn['T4'] = Pieces.T4()
    rtn['F'] = Pieces.F()
    rtn['I'] = Pieces.I()
    rtn['L'] = Pieces.L()
    rtn['N'] = Pieces.N()
    rtn['P'] = Pieces.P()
    rtn['T'] = Pieces.T()
    rtn['U'] = Pieces.U()
    rtn['V'] = Pieces.V()
    rtn['W'] = Pieces.W()
    rtn['X'] = Pieces.X()
    rtn['Y'] = Pieces.Y()
    rtn['Z'] = Pieces.Z()
    return rtn

def initHand():
    """Return an initial hand with all pieces set to True."""
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

def startCorner(color):
    """Return a list with the starting corner for the given color."""
    # NOTE: At some point this should be changed so play order goes clockwise.
    corners = list()
    if color == 1:
        corners.append(np.array([[-1,0],[-1,0]]))
    if color == 2:
        corners.append(np.array([[-1,0],[Gamestate.boardsize, Gamestate.boardsize-1]]))
    if color == 3:
        corners.append(np.array([[Gamestate.boardsize, Gamestate.boardsize-1],
                                 [Gamestate.boardsize, Gamestate.boardsize-1]]))
    if color == 4:
        corners.append(np.array([[Gamestate.boardsize, Gamestate.boardsize-1],[-1,0]]))
    return corners

def initBoard():
    """Returns an empty board"""
    board = np.zeros((Gamestate.boardsize,Gamestate.boardsize),dtype=int)
    return board

class Gamestate:
    """A game state in Blokus, with hands, board, turn etc."""

    referenceHand = initRefHand()
    boardsize = 20

    def __init__(self, blue = 'default', yellow = 'default', red = 'default',
                 green = 'default',
                 bcorners = 'default',
                 ycorners = 'default',
                 rcorners = 'default',
                 gcorners = 'default',
                 board = 'default', turn = 1, passCount = 0,
                 lastPlayed = 'default'):
        """ Initialize a gamestate with given parameters, or a default gamestate if none are provided."""
        
        if blue == 'default':
            self.blue = initHand()
        else:
            self.blue = blue
            
        if yellow == 'default':
            self.yellow = initHand()
        else:
            self.yellow = yellow

        if red == 'default':
            self.red = initHand()
        else:
            self.red = red

        if green == 'default':
            self.green = initHand()
        else:
            self.green = green

        if bcorners == 'default':
            self.bcorners = startCorner(1)
        else:
            self.bcorners = bcorners

        if ycorners == 'default':
            self.ycorners = startCorner(2)
        else:
            self.ycorners = ycorners

        if rcorners == 'default':
            self.rcorners = startCorner(3)
        else:
            self.rcorners = rcorners

        if gcorners == 'default':
            self.gcorners = startCorner(4)
        else:
            self.gcorners = gcorners

        if board == 'default':
            self.board = initBoard()
        else:
            self.board = board
            
        self.turn = turn
        self.passCount = passCount

        if lastPlayed == 'default':
            self.lastPlayed = [None, None, None, None]
        else:
            self.lastPlayed = lastPlayed

    def duplicate(self):
        """Return a deep copy of this gamestate object."""
        blue = deepcopy(self.blue)
        yellow = deepcopy(self.yellow)
        red = deepcopy(self.red)
        green = deepcopy(self.green)
        bcorners = deepcopy(self.bcorners)
        ycorners = deepcopy(self.ycorners)
        rcorners = deepcopy(self.rcorners)
        gcorners = deepcopy(self.gcorners)
        board = self.board.copy()
        turn = self.turn
        passCount = self.passCount
        lastPlayed = deepcopy(self.lastPlayed)
        return Gamestate(blue, yellow, red, green, bcorners, ycorners, rcorners,
                         gcorners, board, turn, passCount, lastPlayed)

    def equals(self, other):
        """Return true if this gamestate has the same board/turn as other, false otherwise."""
        if self.turn != other.turn:
            return False
        return np.array_equal(self.board, other.board)
    
    def update(self, move):
        """Update gamestate with provided move if legal, else return False"""
        if len(move) != 4: # Then move is a pass
            self.setLastPlayed(None, self.turn)
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
        piece_extremes = Pieces.findExtremes(piece.shape)
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

        # Remove piece played from hand
        self.getHand(self.turn)[name] = False

        # Reset pass count
        self.passCount = 0
    
        # Update lastPlayed
        self.setLastPlayed(name, self.turn)
        
        # Advance turn
        self.advanceTurn()
        
    def moveCheck(self, piece):
        """Return whether a move is legal."""
        
        # Check if one of piece's corners matches an open corner on the board
        bcorners = self.getCorners(self.turn)
        pcorners = piece.corners
        diagonal = False
        for cur in Pieces.splitCornerArray(pcorners):
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

    def moveConflicts(self, p):
        """Return whether a move conflicts with (overlaps or is edge adjacent to) pieces on board."""

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
            if x < 0 or y < 0 or x >= Gamestate.boardsize or y >= Gamestate.boardsize:
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
            if x < (Gamestate.boardsize - 1):
                nears['e'] = np.array([[x+1],[y]])

            if y < (Gamestate.boardsize - 1):
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
        
    def advanceTurn(self):
        """Advance turn value to next player."""
        self.turn = self.turn + 1
        if self.turn == 5:
            self.turn = 1

    def getHand(self, color):
        """Return the hand corresponding to provided color."""
        if color == 1:
            return self.blue
        if color == 2:
            return self.yellow
        if color == 3:
            return self.red
        if color == 4:
            return self.green

    def sortedHand(self, color):
        """Return the hand corresponding to provided color as a list sorted by piece size."""
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

    def getCorners(self, color):
        """Return the corner list corresponding to provided color."""
        if color == 1:
            return self.bcorners
        if color == 2:
            return self.ycorners
        if color == 3:
            return self.rcorners
        if color == 4:
            return self.gcorners

    def updateCorners(self, color, corners):
        """Update color's corner list with provided 2x2n corner matrix."""
        oldList = self.getCorners(color)
        for cur in Pieces.splitCornerArray(corners):
            inv = np.array([[cur[0,1],cur[0,0]],[cur[1,1],cur[1,0]]])
            obliterated = False
            for j in range(0, len(oldList)):
                if np.array_equal(oldList[j],inv):
                    del oldList[j]
                    obliterated = True
                    break
            if -1 in cur or Gamestate.boardsize in cur:
                continue
            if not obliterated:
                oldList.append(cur.copy())

    def setLastPlayed(self, name, color):
        """Set lastPlayed entry corresponding to color to provided piece name."""
        for i in range(1,5):
            if color == i:
                self.lastPlayed[i-1] = name
        
    def colorSet(self, coords, color):
        """Change coordinates in 2xn coordinate matrix to provided color."""
        if not (color in range(1,5)):
            return False
        for i in range(coords[0].size):
            if self.board[coords[1,i]][coords[0,i]] != 0:
                return False
            self.board[coords[1,i]][coords[0,i]] = color
        return True

    def listMoves(self):
        """Get list of possible moves for current player."""
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

        # Finally, add 'pass!' which is always a valid move
        rtn.append('pass!')
        return rtn

    def findPieceMoves(self, p):
        """Return list of possible moves for piece p in current orientation."""
        
        rtn = list()
        bcorners = self.getCorners(self.turn)
        piece_extremes = Pieces.findExtremes(p.shape)
        piece_xmin, piece_ymin = piece_extremes[0], piece_extremes[2]
        
        # For each corner pc on the piece...
        pcorners = p.corners
        for pc in Pieces.splitCornerArray(pcorners):

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

    def canMove(self):
        """Return the first legal move found."""
        hand = self.getHand(self.turn)
        corners = self.getCorners(self.turn)

        # If no corners or no pieces in hand, no moves are possible
        if not (True in hand.values()) or len(corners) == 0:
            return False

        # For each piece, find list of moves for each orientation
        # with findPieceMoves
        sortedHand = self.sortedHand(self.turn)
        for piece in sortedHand:
            canFindPieceMoves = self.canFindPieceMoves(piece)
            if not canFindPieceMoves == False:
                return canFindPieceMoves

            if piece.r90 and piece.r180:
                for i in range(3):
                    piece.rotate(1)
                    canFindPieceMoves = self.canFindPieceMoves(piece)
                    if not canFindPieceMoves == False:
                        return canFindPieceMoves                  
            elif piece.r90 and not piece.r180:
                piece.rotate(1)
                canFindPieceMoves = self.canFindPieceMoves(piece)
                if not canFindPieceMoves == False:
                    return canFindPieceMoves
                
            if piece.chiral:
                piece.flipV()
                canFindPieceMoves = self.canFindPieceMoves(piece)
                if not canFindPieceMoves == False:
                    return canFindPieceMoves
                if piece.r90 and piece.r180:
                    for i in range(3):
                        piece.rotate(1)
                        canFindPieceMoves = self.canFindPieceMoves(piece)
                        if not canFindPieceMoves == False:
                            return canFindPieceMoves
                elif piece.r90 and not piece.r180:
                    piece.rotate(1)
                    canFindPieceMoves = self.canFindPieceMoves(piece)
                    if not canFindPieceMoves == False:
                        return canFindPieceMoves
        return False

    def canFindPieceMoves(self, p):
        """Return first legal move found for piece p in current orientation."""

        bcorners = self.getCorners(self.turn)
        piece_extremes = Pieces.findExtremes(p.shape)
        piece_xmin, piece_ymin = piece_extremes[0], piece_extremes[2]
        
        # For each corner pc on the piece...
        pcorners = p.corners
        for pc in Pieces.splitCornerArray(pcorners):

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
                        return (p.name, p.orientation, piece_xmin, piece_ymin) 

        return False

    def isTerminal(self):
        """Return true if gamestate is terminal (four consecutive passes), false otherwise."""
        if self.passCount >= 4:
            return True
        return False

    def getScores(self):
        """Return list of scores."""
        scores = [0,0,0,0]
        for i in range(1,5):
            hand = self.getHand(i)
            for name, val in hand.items():
                if val:
                    scores[i-1] = scores[i-1] - Gamestate.referenceHand[name].size
            if not (True in hand) and self.lastPlayed[i-1]:
                scores[i-1] = scores[i-1] - 5
        return scores
        
    def printScores(self):
        """Print current scores."""

        scores = self.getScores()
        print("Final scores:")
        print("Blue:")
        print scores[0]
        print("Yellow:")
        print scores[1]
        print("Red:")
        print scores[2]
        print("Green:")
        print scores[3]
    
    def printBoard(self):
        """Print current board."""
        print self.board
        
    def printHand(self, i):
        """Print a player's hand."""
        hand = self.getHand(i)
        for name, val in hand.items():
            if val:
                sys.stdout.write(name + ' ')
        sys.stdout.write("\n")

    def printSortedHand(self, i):
        """Print a player's hand sorted by piece size."""
        sortedhand = self.sortedHand(i)
        for p in sortedhand:
            sys.stdout.write(p.name + ' ')
        sys.stdout.write("\n")
