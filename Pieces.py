class Corner:
    '''Set of two coordinates represents an available corner on an unplaced piece'''
    def __init__(self, x1, y1, x2, y2):
        #x1, y1 is the square ON the piece and x2, y2 is the square BY the piece
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Piece:
    '''Generic piece type which specific pieces will extend'''
    
    #r90 (bool): Does piece lack fourfold rotational symmetry? 
    #r180 (bool): Does piece lack twofold rotational symmetry? 
    #chiral (bool): Is piece chiral?
    #size (int): # squares in the piece
    #shape (2d list of booleans): Current configuration of piece
    #corners (1d list of corners): .. Corners

    # flips piece horizontally
    def flipH(self):
        #Flip corners
        for i in range(len(self.corners)):
            self.corners[i].x1 = len(self.shape) - 1 - self.corners[i].x1
            self.corners[i].x2 = len(self.shape) - 1 - self.corners[i].x2
        #Then flip piece itself
        original = self.shape[:]
        self.shape.reverse()
        if original == self.shape:
            return False
        else:
            return True
        
    # flips piece vertically
    def flipV(self):
        #Flip corners
        for i in range(len(self.corners)):
            self.corners[i].y1 = len(self.shape[0]) - 1 - self.corners[i].y1
            self.corners[i].y2 = len(self.shape[0]) - 1 - self.corners[i].y2
        #Then flip piece itself
        original = self.shape[:]
        for i in range(len(self.shape)):
            self.shape[i].reverse()
        if original == self.shape:
            return False
        else:
            return True

    # rotates piece 90*turns degrees counterclockwise
    # returns false if turns is not between one and three
    # or if rotation makes no change
    def rotate(self, turns):
        if turns == 1 and self.r90:
            rotated = list()
            for i in range(len(self.shape[0])): #y-coord in original array
                rotated.append(list())
                for j in range(len(self.shape)): #x-coord in original array
                    rotated[i].insert(0, self.shape[j][i])
            self.shape = rotated
            return True
        elif turns == 2 and self.r180:
            self.flipH()
            self.flipV()
            return True
        elif turns == 3 and self.r90:
            rotated = list()
            for i in range(len(self.shape[0])): #y-coord in original array
                rotated.insert(0, list())
                for j in range(len(self.shape)): #x-coord in original array
                    rotated[0].add(self.shape[j][i])
            self.shape = rotated
            return True
        else:
            return False

    # checks if a given array matches any permutation of this piece
    # shape is a 2d list of bools
    def isThisPiece(self, compare):
        original = self.shape[:]
        
        if self.shape == compare:
            return True
        
        if self.r90 and self.r180:
            for i in range(3):
                self.rotate(1)
                if self.shape == compare:
                    return True
        elif self.r90 and not self.r180:
            self.rotate(1)
            if self.shape == compare:
                return True

        if self.chiral:
            if not self.flipV():
                self.flipH()

            if self.shape == compare:
                return True
        
            if self.r90 and self.r180:
                for i in range(3):
                    self.rotate(1)
                    if self.shape == compare:
                        return True
            elif self.r90 and not self.r180:
                self.rotate(1)
                if self.shape == compare:
                    return True
            

    # return a string representation of the piece
    def __repr__(self):
        return self.shape.__repr__()

# Individual piece definitions
    
class F(Piece):
    def __init__(self):
        self.shape = [[False, True, False],[True, True, True],[True, False, False]]
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class I(Piece):
    def __init__(self):
        self.shape = [[True, True, True, True, True]]
        self.r90 = True
        self.r180 = False
        self.chiral = False
        self.size = 5

class L(Piece):
    def __init__(self):
        self.shape = [[True, True, True, True],[False, False, False, True]]
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class N(Piece):
    def __init__(self):
        self.shape = [[True, True, True, False],[False, False, True, True]]
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class P(Piece):
    def __init__(self):
        self.shape = [[True, True, True],[True, True, False]]
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class T(Piece):
    def __init__(self):
        self.shape = [[True, False, False],[True, True, True],[True, False, False]]
        self.r90 = True
        self.r180 = True
        self.chiral = False
        self.size = 5

class U(Piece):
    def __init__(self):
        self.shape = [[True, True],[False, True],[True, True]]
        self.r90 = True
        self.r180 = True
        self.chiral = False
        self.size = 5

class V(Piece):
    def __init__(self):
        self.shape = [[True, True, True],[False, False, True],[False, False, True]]
        self.r90 = True
        self.r180 = True
        self.chiral = False
        self.size = 5

class W(Piece):
    def __init__(self):
        self.shape = [[True, True, False],[False, True, True],[False, False, True]]
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class X(Piece):
    def __init__(self):
        self.shape = [[False, True, False],[True, True, True],[False, True, False]]
        self.r90 = False
        self.r180 = False
        self.chiral = False
        self.size = 5

class Y(Piece):
    def __init__(self):
        self.shape = [[True, True, True, True],[False, True, False, False]]
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class Z(Piece):
    def __init__(self):
        self.shape = [[True, False, False],[True, True, True],[False, False, True]]
        self.r90 = True
        self.r180 = False
        self.chiral = True
        self.size = 5

class I4(Piece):
    def __init__(self):
        self.shape = [[True, True, True, True]]
        self.r90 = True
        self.r180 = False
        self.chiral = False
        self.size = 4

class L4(Piece):
    def __init__(self):
        self.shape = [[True, True, True],[False, False, True]]
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 4

class N4(Piece):
    def __init__(self):
        self.shape = [[True, True, False],[False, True, True]]
        self.r90 = True
        self.r180 = False
        self.chiral = True
        self.size = 4

class O(Piece):
    def __init__(self):
        self.shape = [[True, True],[True, True]]
        self.r90 = False
        self.r180 = False
        self.chiral = False
        self.size = 4

class T4(Piece):
    def __init__(self):
        self.shape = [[True, True, True],[False, True, False]]
        self.r90 = True
        self.r180 = True
        self.chiral = False
        self.size = 4

class I3(Piece):
    def __init__(self):
        self.shape = [[True, True, True]]
        self.r90 = True
        self.r180 = False
        self.chiral = False
        self.size = 3

class V3(Piece):
    def __init__(self):
        self.shape = [[True, True],[False, True]]
        self.r90 = True
        self.r180 = True
        self.chiral = False
        self.size = 3

class Two(Piece):
    def __init__(self):
        self.shape = [[True, True]]
        self.r90 = True
        self.r180 = False
        self.chiral = False
        self.size = 2

class One(Piece):
    def __init__(self):
        self.shape = [[True]]
        self.r90 = False
        self.r180 = False
        self.chiral = False
        self.size = 1
