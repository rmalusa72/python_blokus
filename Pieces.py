import numpy as np

# Coordinates are 2x1 matrices
# Corners are 2x2n matrices where each column is a point
# Piece shapes are 2xn matrices where each column is a point 
# Transformation matrices are 2x2 matrices where Ax = T(x)

# Finds the minimum and maximum x and y in a 2xn array of points
def findExtremes(points):
    xmin = xmax = points[0,0]
    ymin = ymax = points[1,0]

    for i in range(0, points[0].size):
        curx = points[0,i]
        cury = points[1,i]
        if curx < xmin:
            xmin = curx
        if curx > xmax:
            xmax = curx
        if cury < ymin:
            ymin = cury
        if cury > ymax:
            ymax = cury
    return (xmin, xmax, ymin, ymax)
    
# Converts each point in a 2xn array of points into a
# 'true' at the corresponding point in a 2d array of booleans
def toBoolArray(points):
    #Get min and max x and y
    xmin, xmax, ymin, ymax = findExtremes(points)

    # Find width and height
    width = xmax - xmin + 1
    height = ymax - ymin + 1

    # Make 'blank' 2d boolean array (all false) of correct size
    shape = np.zeros((height, width), dtype = bool)

    # Switch appropriate points to True
    for i in range(0, points[0].size):
        shape[points[1,i] - ymin][points[0,i] - xmin] = True

    return shape

class Piece:
    '''Generic piece type extended by specific pieces'''

    # r90 (bool): Does piece lack fourfold rotational symmetry?
    # r180 (bool): Does piece lack twofold rotational symmetry?
    # chiral (bool): Is piece chiral?
    # shape: 2xn array of coordinates where n = size of piece
    # corners: 2x2c array of coordinates where c = number of corners

    # flips piece horizontally
    # returns True if the shape has changed, false otherwise
    def flipH(self):
        hflip = np.array([[-1, 0],[0,1]])

        # Flip corners
        self.corners = np.dot(hflip, self.corners)

        # Save original shape for comparison, then flip shape
        original = np.copy(self.shape)
        self.shape = np.dot(hflip, self.shape)

        o = toBoolArray(original)
        s = toBoolArray(self.shape)
        return not np.array_equal(o,s)

    # flips piece vertically
    def flipV(self):
        vflip = np.array([[1,0],[0,-1]])

        # Flip corners
        self.corners = np.dot(vflip, self.corners)

        # Save original self for comparison, then flip shape
        original = np.copy(self.shape)
        self.shape = np.dot(vflip, self.shape)

        o = toBoolArray(original)
        s = toBoolArray(self.shape)
        return not np.array_equal(o,s)

    # rotates piece 90*turns degrees ccw
    # NOTE: rotation matrices are for cw turns bc of y axis pointing down
    # in matrix indexing
    # returns false if turns is not between one and three
    # or if rotation makes no change
    def rotate(self, turns):
        if turns == 1 and self.r90:
            rmat = np.array([[0,1],[-1,0]])
            self.corners = np.dot(rmat, self.corners)
            self.shape = np.dot(rmat, self.shape)
            return True
        elif turns == 2 and self.r180:
            rmat = np.array([[-1,0],[0,-1]])
            self.corners = np.dot(rmat, self.corners)
            self.shape = np.dot(rmat, self.shape)
            return True
        elif turns == 3 and self.r90:
            rmat = np.array([[0,-1],[1,0]])
            self.corners = np.dot(rmat, self.corners)
            self.shape = np.dot(rmat, self.shape)
            return True
        else:
            return False

    def translate(self, x,y):
        self.shape[0] += x
        self.shape[1] += y
        self.corners[0] += x
        self.corners[1] += y

    # checks if a given array matches any permutation of this piece
    # compare is a 2d array of bools
    def isThisPiece(self, compare):
        
        boolshape = toBoolArray(self.shape)
        if np.array_equal(boolshape, compare):
            return True

        if self.r90 and self.r180:
            for i in range(3):
                self.rotate(1)
                boolshape = toBoolArray(self.shape)
                if np.array_equal(boolshape, compare):
                    return True
        elif self.r90 and not self.r180:
            self.rotate(1)
            boolshape = toBoolArray(self.shape)
            if np.array_equal(boolshape, compare):
                return True

        if self.chiral:
            if not self.flipV():
                self.flipH()

            boolshape = toBoolArray(self.shape)
            if np.array_equal(boolshape, compare):
                return True

            if self.r90 and self.r180:
                for i in range(3):
                    self.rotate(1)
                    boolshape = toBoolArray(self.shape)
                    if np.array_equal(boolshape, compare):
                        return True
            elif self.r90 and not self.r180:
                self.rotate(1)
                boolshape = toBoolArray(self.shape)
                if np.array_equal(boolshape, compare):
                    return True
        
    def __repr__(self):
        return toBoolArray(self.shape).__repr__()


class F(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,1,2,1],
                               [0,0,1,1,2]])
        self.corners = np.array([[0,-1,1,2,1,0,1,2,0,-1,2,3,2,3],
                                 [0,-1,0,-1,2,3,2,3,0,1,1,0,1,2]])
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class I(Piece):
    def __init__(self):
        self.shape = np.array([[0,0,0,0,0],
                               [0,1,2,3,4]])
        self.corners = np.array([[0,-1,0,1,0,-1,0,1],
                                 [0,-1,0,-1,4,5,4,5]])
        self.r90 = True
        self.r180 = False
        self.chiral = False
        self.size = 5

class L(Piece):
    def __init__(self):
        self.shape = np.array([[0,0,0,0,1],
                               [0,1,2,3,0]])
        self.corners = np.array([[0,-1,1,2,1,2,0,-1,0,1],
                                 [0,-1,0,-1,0,1,3,4,3,4]])
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class N(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,2,2,3],[0,0,0,1,1]])
        self.corners = np.array([[0,-1,0,-1,2,3,2,1,3,4,3,4],
                                 [0,-1,0,1,0,-1,1,2,1,0,1,2]])
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class P(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,0,1,0],
                               [0,0,1,1,2]])
        self.corners = np.array([[0,-1,1,2,1,2,0,-1,0,1],
                                 [0,-1,0,-1,1,2,2,3,2,3]])
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class T(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,2,1,1],
                               [0,0,0,1,2]])
        self.corners = np.array([[0,-1,0,-1,2,3,2,3,1,0,1,2],
                                 [0,-1,0,1,0,-1,0,1,2,3,2,3]])
        self.r90 = True
        self.r180 = True
        self.chiral = False
        self.size = 5

class U(Piece):
    def __init__(self):
        self.shape = np.array([[0,0,1,2,2],
                               [0,1,1,1,0]])
        self.corners = np.array([[0,-1,0,1,0,-1,2,3,2,1,2,3],
                                 [0,-1,0,-1,1,2,1,2,0,-1,0,-1]])
        self.r90 = True
        self.r180 = True
        self.chiral = False
        self.size = 5

class V(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,0,2,0],
                               [0,0,1,0,2]])
        self.corners = np.array([[0,-1,2,3,2,3,0,-1,0,1],
                                 [0,-1,0,-1,0,1,2,3,2,3]])
        self.r90 = True
        self.r180 = True
        self.chiral = False
        self.size = 5

class W(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,1,2,2],
                               [0,0,1,1,2]])
        self.corners = np.array([[0,-1,0,-1,1,2,1,0,2,3,2,1,2,3],
                                 [0,-1,0,1,0,-1,1,2,1,0,2,3,2,3]])
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class X(Piece):
    def __init__(self):
        self.shape = np.array([[1,0,1,2,1],
                               [0,1,1,1,2]])
        self.corners = np.array([[1,0,1,2,0,-1,0,-1,1,0,1,2,2,3,2,3],
                                 [0,-1,0,-1,1,0,1,2,2,3,2,3,1,0,1,2]])
        self.r90 = False
        self.r180 = False
        self.chiral = False
        self.size = 5

class Y(Piece):
    def __init__(self):
        self.shape = np.array([[0,0,0,0,1],
                               [0,1,2,3,1]])
        self.corners = np.array([[0,-1,0,1,1,2,1,2,0,-1,0,1],
                                 [0,-1,0,-1,1,0,1,2,3,4,3,4]])
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 5

class Z(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,1,1,2],
                               [0,0,1,2,2]])
        self.corners = np.array([[0,-1,0,-1,1,2,1,0,2,3,2,3],
                                 [0,-1,0,1,0,-1,2,3,2,3,2,1]])
        self.r90 = True
        self.r180 = False
        self.chiral = True
        self.size = 5

class I4(Piece):
    def __init__(self):
        self.shape = np.array([[0,0,0,0],
                               [0,1,2,3]])
        self.corners = np.array([[0,-1,0,1,0,-1,0,1],
                                 [0,-1,0,-1,3,4,3,4]])
        self.r90 = True
        self.r180 = False
        self.chiral = False
        self.size = 4

class L4(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,0,0],
                               [0,0,1,2]])
        self.corners = np.array([[0,-1,1,2,1,2,0,-1,0,1],
                                 [0,-1,0,-1,0,1,2,3,2,3]])
        self.r90 = True
        self.r180 = True
        self.chiral = True
        self.size = 4

class N4(Piece):
    def __init__(self):
        self.shape = np.array([[0,0,1,1],
                               [0,1,1,2]])
        self.corners = np.array([[0,-1,0,1,0,-1,1,2,1,0,1,2],
                                 [0,-1,0,-1,1,2,1,0,2,3,2,3]])
        self.r90 = True
        self.r180 = False
        self.chiral = True
        self.size = 4

class O(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,0,1],
                               [0,0,1,1]])
        self.corners = np.array([[0,-1,1,2,0,-1,1,2],
                                 [0,-1,0,-1,1,2,1,2]])
        self.r90 = False
        self.r180 = False
        self.chiral = False
        self.size = 4

class T4(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,1,2],
                               [0,0,1,0]])
        self.corners = np.array([[0,-1,2,3,1,0,1,2],
                                 [0,-1,0,-1,1,2,1,2]])
        self.r90 = True
        self.r180 = True
        self.chiral = False
        self.size = 4

class I3(Piece):
    def __init__(self):
        self.shape = np.array([[0,0,0],
                               [0,1,2]])
        self.corners = np.array([[0,-1,0,1,0,-1,0,1],
                                 [0,-1,0,-1,2,3,2,3]])
        self.r90 = True
        self.r180 = False
        self.chiral = False
        self.size = 3

class V3(Piece):
    def __init__(self):
        self.shape = np.array([[0,1,1],
                               [0,0,1]])
        self.corners = np.array([[0,-1,0,-1,1,2,1,0,1,2],
                                 [0,-1,0,1,0,-1,1,2,1,2]])
        self.r90 = True
        self.r180 = True
        self.chiral = False
        self.size = 3

class Two(Piece):
    def __init__(self):
        self.shape = np.array([[0,0],
                               [0,1]])
        self.corners = np.array([[0,-1,0,1,0,-1,0,1],
                                 [0,-1,0,-1,1,2,1,2]])
        self.r90 = True
        self.r180 = False
        self.chiral = False
        self.size = 2

class One(Piece):
    def __init__(self):
        self.shape = np.array([[0],
                               [0]])
        self.corners = np.array([[0,-1,0,1,0,1,0,-1],
                                 [0,-1,0,-1,0,1,0,1]])
        self.r90 = False
        self.r180 = False
        self.chiral = False
        self.size = 1


        
