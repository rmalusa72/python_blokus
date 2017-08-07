# BLOKUSFUNCTIONS.PY
# Functions useful for the other classes
import numpy as np

def findExtremes(points):
    """Return the minimum and maximum x and y from a 2xn array of points."""
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

def toBoolArray(points):
    """Return a 2d boolean array in the shape of the provided 2xn point array."""
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

def splitCornerArray(corners):
    """Return a list containing views of each 2x2 corner in a 2x2n array of corners"""
    # NOTE: these will change as the piece moves! Make a copy to save them
    rtn = list()
    numCorners = corners[0].size/2
    for i in range(0, numCorners):
        cur = corners[:,2*i:2*(i+1)]
        rtn.append(cur)
    return rtn

