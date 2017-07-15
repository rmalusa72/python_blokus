import numpy as np

# Coordinates are 2x1 matrices
# Corners are 2x2n matrices where each column is a point
# Piece shapes are 2xn matrices where each column is a point 
# Transformation matrices are 2x2 matrices where Ax = T(x)

# Converts each point in a 2xn array of points into a
# 'true' at the corresponding point in a 2d array of booleans
def toBoolArray(points):
    #Find min and max x and y
    xmin = xmax = points[0][0]
    ymin = ymax = points[1][0]

    for i in range(0, points[0].size):
        curx = points[0][i]
        cury = points[1][i]
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

    # Make 'blank' 2d boolean array (all false) of correct size
    shape = np.zeros((height, width), dtype = bool)

    # Switch appropriate points to True
    for i in range(0, points[0].size):
        shape[points[1][i] - ymin][points[0][i] - xmin] = True

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


        
