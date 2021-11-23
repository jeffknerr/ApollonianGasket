#! /usr/bin/python3

"""
trying to make pretty pictures...
J. Knerr
Spring 2021
"""

# https://en.wikipedia.org/wiki/Apollonian_gasket
# https://www.tcd.ie/Physics/research/groups/foams/media/gasket.pdf
# https://arxiv.org/abs/math/0101066

import math
import cmath
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import mycircles
import click


@click.command()
@click.option("--x2", default=0.3,
              help="x coordinate of circle #2 (e.g., 0.3 or 0.5)")
@click.option("--maxdepth", default=4,
              help="max recursion depth (e.g., 3, 7, 2)")
def main(x2, maxdepth):
    """apollonian gasket code"""
    # recursion control...
    level = 0
    # maxdepth = 5
    # store all circles, plot at the end
    allcircles = {}
    # first circle C1 that surrounds all the others
    x1 = 0
    y1 = 0
    r1 = 1
    a = -1
    Cobj = mycircles.Circle(x1, y1, r1)
    allcircles[hash(Cobj)] = Cobj
    # for second circle C2, let user pick x location such that 0>x2<1
    y2 = 0
    # x2 = getx("x2", 0, 1)
    r2 = 1 - x2
    b = 1/r2
    Cobj = mycircles.Circle(x2, y2, r2)
    allcircles[hash(Cobj)] = Cobj
    # now find C3, assuming it also has y3 = 0
    r3 = 1 - r2
    c = 1/r3
    x3 = x2 - r2 - r3
    y3 = 0
    Cobj = mycircles.Circle(x3, y3, r3)
    allcircles[hash(Cobj)] = Cobj
    # A = bend*center = a*(x1+y1j)
    A = a*(x1+y1*1j)
    B = b*(x2+y2*1j)
    C = c*(x3+y3*1j)
    solve(a, A, b, B, c, C, level, maxdepth, allcircles)
    plot(allcircles)


def solve(a, A, b, B, c, C, level, maxdepth, allcircles):
    """given 3 circles, find 2 new ones"""
    if level > maxdepth:
        return
    dp, dm = descartes(a, b, c)
    Dplus = (A + B + C) + (2*cmath.sqrt(A*B + A*C + B*C))
    Dminus = (A + B + C) - (2*cmath.sqrt(A*B + A*C + B*C))
    # 4 possible solutions, only two of them are tangent to original 3
    # checkAll(A,a,B,b,C,c,dp,dm,Dplus,Dminus)
    # find/add two new ones to dictionary by doing tangent checks...
#   print("level:", level)
#   printc("ABC:",A,a,B,b,C,c)
#   printc("pp,mp,pm,mm:",Dplus,dp,Dminus,dp,Dplus,dm,Dminus,dm)
#   input()
    for d, D in [(dp, Dplus),  (dp, Dminus), (dm, Dplus), (dm, Dminus)]:
        if not tangent(a, A, b, B, c, C, d, D):
            pass  # don't include this solution....don't recur on it
        elif d < 0:
            pass  # don't allow negative radii ???
        else:
            Dx = D.real/d
            Dy = D.imag/d
            Cobj = mycircles.Circle(Dx, Dy, 1/d)
            if hash(Cobj) not in allcircles:
                allcircles[hash(Cobj)] = Cobj
                level = level + 1
                # recur on 3 new possibilities
                solve(a, A, b, B, d, D, level, maxdepth, allcircles)
                solve(a, A, c, C, d, D, level, maxdepth, allcircles)
                solve(c, C, b, B, d, D, level, maxdepth, allcircles)


def printc(text, X, x, Y, y, Z, z, W=(99+99j), w=99):
    """print circle details"""
    xi = (X/x).imag
    xr = (X/x).real
    yi = (Y/y).imag
    yr = (Y/y).real
    zi = (Z/z).imag
    zr = (Z/z).real
    wi = (W/w).imag
    wr = (W/w).real
    if w == 99:
        print("%s: %5.2f, %5.2f %5.2f |%5.2f, %5.2f %5.2f |%5.2f, %5.2f %5.2f" %
              (text, xr, xi, 1/x, yr, yi, 1/y, zr, zi, 1/z))
    else:
        print("%s: %5.2f, %5.2f %5.2f |%5.2f, %5.2f %5.2f |%5.2f, %5.2f %5.2f |%5.2f, %5.2f %5.2f" %
              (text, xr, xi, 1/x, yr, yi, 1/y, zr, zi, 1/z, wr, wi, 1/w))


def getx(prompt, minx, maxx):
    """get an x float"""
    while True:
        try:
            x = input(prompt+": ")
            x = float(x)
            if x > minx and x < maxx:
                return x
            else:
                print("Please enter x between %.1f and %.1f..." % (minx, maxx))
        except ValueError:
            print("please enter a float...")


def descartes(a, b, c):
    """
    solve the Descartes circle equation for d:
       a**2 + b**2 + c**2 + d**2 = 0.5(a+b+c+d)**2
    given a, b, c.

    If you rearrange this into
       (x)d**2 + (y)d + (z) = 0
    with x=1, y=-2(a+b+c), z=(a**2 + b**2 + c**2) - 2(ab + ac + bc)
    and plug into the quadratic formula (normally abc, but
    here changed to xyz):
       (-y +/- sqrt(y**2 - 4xz))/2x
    that can all be simplified to this:
       d = a + b + c +/- 2*sqrt(ab + ac + bc)
    """
    radicand = a*b + a*c + b*c
    epsilon = 1.0e-4
    if abs(radicand) < epsilon:
        radicand = 0
    try:
        plus = a + b + c + 2*math.sqrt(radicand)
        minus = a + b + c - 2*math.sqrt(radicand)
        return plus, minus
    except ValueError:
        print("got value error trying sqrt of %f..." % (radicand))
        return None


def tangent(a, A, b, B, c, C, d, D):
    """return True if circles are all tangent to each other"""
    return twoTangent(a, A, d, D) and \
        twoTangent(b, B, d, D) and \
        twoTangent(c, C, d, D)


def twoTangent(a, A, b, B):
    """return True if two circles are tangent"""
    r1 = abs(1/a)
    r2 = abs(1/b)
    x1 = A.real/a
    y1 = A.imag/a
    x2 = B.real/b
    y2 = B.imag/b
    d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    # allow for approx equal
    epsilon = 1.0e-4
    diff1 = abs(d-(r1+r2))  # test for tangent OUTSIDE circle
    diff2 = abs(d-abs(r1-r2))  # test for tangent INSIDE circle
    return (diff1 <= epsilon) or (diff2 <= epsilon)


def checkAll(A, a, B, b, C, c, dp, dm, Dplus, Dminus):
    """check which ones are tangent"""
    print("Dpdp: ", tangent(a, A, b, B, c, C, dp, Dplus))
    print("Dpdm: ", tangent(a, A, b, B, c, C, dp, Dminus))
    print("Dmdp: ", tangent(a, A, b, B, c, C, dm, Dplus))
    print("Dmdm: ", tangent(a, A, b, B, c, C, dm, Dminus))
    print("-"*20)


def mysort(allcircles):
    """return keys, sorted by circle radius (largest first)"""
    # note: need to do my own sort, since the Circle objects already
    # have an __eq__ method that is not related to radius...
    keys = list(allcircles.keys())
    values = list(allcircles.values())
    for i in range(1, len(keys)):
        key = keys[i]                # save current key
        value = values[i]            # save current value
        posn = i
        while posn > 0 and value.getR() > values[posn-1].getR():
            values[posn] = values[posn-1]  # move item right one position
            keys[posn] = keys[posn-1]
            posn = posn - 1
        values[posn] = value     # put it back at the end, in correct spot
        keys[posn] = key         # put it back at the end, in correct spot
    return keys


def plot(allcircles):
    """plot the circles"""
    fig, ax = plt.subplots()
    patches = []
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.grid(False)
    ax.set_aspect(1)
    ax.set_title("Apollonian Gasket")

    # sort keys based on circle radius, so we can plot largest first
    keys = mysort(allcircles)
#   keys.reverse()
    for key in keys[0:len(keys) - 1]:    # remove duplicates???
        cobj = allcircles[key]
        print(cobj)
# todo: why are there similar circles in the list??? (0,0,-1) <-- 3 of these??
        x = cobj.getX()
        y = cobj.getY()
        radius = cobj.getR()
        circle = Circle((x, y), radius)
        patches.append(circle)
    mycolors = ["red", "green", "blue", "cyan", "pink", "orange"]
    collection = PatchCollection(patches, edgecolor="black",
                                 facecolor=mycolors,
                                 alpha=1.0)
    ax.add_collection(collection)
    plt.show()


main()
