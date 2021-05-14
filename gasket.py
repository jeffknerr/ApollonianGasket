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
import circles


def main():
    """apollonian gasket code"""
    # recursion control...
    level = 0
    maxdepth = 5
    # store all circles, plot at the end
    allcircles = {}
    # first circle C1 that surrounds all the others
    x1 = 0
    y1 = 0
    r1 = 1
    a = -1
    Cobj = circles.Circle(x1, y1, r1)
    allcircles[hash(Cobj)] = Cobj
    # for second circle C2, let user pick x location such that 0>x2<1
    y2 = 0
    x2 = getx("x2", 0, 1)
    r2 = 1 - x2
    b = 1/r2
    Cobj = circles.Circle(x2, y2, r2)
    allcircles[hash(Cobj)] = Cobj
    # now find C3, assuming it also has y3 = 0
    r3 = 1 - r2
    c = 1/r3
    x3 = x2 - r2 - r3
    y3 = 0
    Cobj = circles.Circle(x3, y3, r3)
    allcircles[hash(Cobj)] = Cobj
    # A = bend*center = a*(x1+y1j)
    A = a*(x1+y1*1j)
    B = b*(x2+y2*1j)
    C = c*(x3+y3*1j)
    solve(a, A, b, B, c, C, level, maxdepth, allcircles)
    plot(allcircles)


def solve(a, A, b, B, c, C, level, maxdepth, allcircles):
    """given 3 circles, find 2 new ones"""
    dp, dm = descartes(a, b, c)
    d = dp   # ??? only use one???
    Dplus = (A + B + C) + 2*cmath.sqrt(A*B + A*C + B*C)
    Dminus = (A + B + C) - 2*cmath.sqrt(A*B + A*C + B*C)
    Dyplus = Dplus.imag/d
    Dyminus = Dminus.imag/d
    Dxplus = Dplus.real/d
    Dxminus = Dminus.real/d
    # add two new ones to dictionary
    Cobj = circles.Circle(Dxplus, Dyplus, 1/d)
    allcircles[hash(Cobj)] = Cobj
    Cobj = circles.Circle(Dxminus, Dyminus, 1/d)
    allcircles[hash(Cobj)] = Cobj
    if level > maxdepth:
        return
    else:
        level = level + 1
        # recur on 6 new possibilities
        solve(a, A, b, B, d, Dplus, level, maxdepth, allcircles)
        solve(a, A, c, C, d, Dplus, level, maxdepth, allcircles)
        solve(c, C, b, B, d, Dplus, level, maxdepth, allcircles)
        solve(a, A, b, B, d, Dminus, level, maxdepth, allcircles)
        solve(a, A, c, C, d, Dminus, level, maxdepth, allcircles)
        solve(c, C, b, B, d, Dminus, level, maxdepth, allcircles)

#   print("plus: dx = %.2f  dy = %.2f" % (Dxplus, Dyplus))
#   print("minus: dx = %.2f  dy = %.2f" % (Dxminus, Dyminus))


def plot(allcircles):
    """plot the circles"""
    fig, ax = plt.subplots()
    patches = []
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.grid(True)

    for key in allcircles:
        cobj = allcircles[key]
        x = cobj.getX()
        y = cobj.getY()
        radius = cobj.getR()
        circle = Circle((x, y), radius)
        patches.append(circle)

    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)
    plt.show()


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
    epsilon = 1.0e-8
    if abs(radicand) < epsilon:
        radicand = 0
    try:
        plus = a + b + c + 2*math.sqrt(radicand)
        minus = a + b + c - 2*math.sqrt(radicand)
        return plus, minus
    except ValueError:
        print("got value error trying sqrt of %d..." % (radicand))
        return None


main()
