"""
circle packing...

J. Knerr
Nov 2021
"""

from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import mycircles
import random
import math


def main():
    """the main function"""
    circles = []
    N = 10000
    maxr = .5
    # N = ...
    # max radius = ...
    # for i in range(N)
    #   pick random point
    #   make sure it's not in a circle already
    #   "create" small circle
    #   while small circle doesn't touch/intersect with any others
    #      make it bigger, up to a max radius
    #   draw the "circle" using random nums and AG
    x = 2*random.random() - 1
    y = 2*random.random() - 1
    r = random.random() * maxr
    Cobj = mycircles.Circle(x, y, r)
    circles.append(Cobj)
    for i in range(N):
        x = 2*random.random() - 1
        y = 2*random.random() - 1
        point = (x, y)
        if not inside(point, circles):
            r = grow(point, circles, maxr)
            Cobj = mycircles.Circle(x, y, r)
            circles.append(Cobj)
    plot(circles, N)


def grow(point, circles, maxr):
    """
    calculate and return largest radius for this circle, centered at
    point, such that it doesn't intersect with other circles (and
    doesn't exceed the size of maxr)
    """
    radius = 0.0
    step = 0.01
    while radius < maxr:
        radius += step
        if intersects(point, radius, circles):
            return radius - step
    return maxr


def intersects(point, radius, circles):
    """return True if new circle hits any of the circles"""
    for c in circles:
        cx = c.getX()
        cy = c.getY()
        cr = c.getR()
        px = point[0]
        py = point[1]
        d = distance(cx, cy, px, py)
        if d <= cr + radius:
            return True
    return False


def inside(point, circles):
    """return True if point is inside any of the circles"""
    for c in circles:
        cx = c.getX()
        cy = c.getY()
        cr = c.getR()
        px = point[0]
        py = point[1]
        d = distance(cx, cy, px, py)
        if d <= cr:
            return True
    return False


def distance(x1, y1, x2, y2):
    """return distance between two points"""
    d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return d


def plot(allcircles, N):
    """plot the circles"""
    fig, ax = plt.subplots()
    patches = []
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.grid(False)
    ax.set_aspect(1)
    ax.set_title("Fun With %d Circles..." % N)

    for cobj in allcircles:
        x = cobj.getX()
        y = cobj.getY()
        radius = cobj.getR()
        # this is the matplotlib Circle object
        circle = Circle((x, y), radius)
        patches.append(circle)
    greys = ["white", "black", "LightSlateGrey", "grey", "LightGrey",
             "DarkGrey", "DimGrey", "SlateGrey"]
    collection = PatchCollection(patches, edgecolor="black",
                                 facecolor=greys)
    ax.add_collection(collection)
    plt.show()


main()
