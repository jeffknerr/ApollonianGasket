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


def main():
    """apollonian gasket code"""
    # first circle C1 that surrounds all the others
    x1 = 0
    y1 = 0
    a = -1
    # for second circle C2, let user pick x location such that 0>x2<1
    y2 = 0
    x2 = getx("x2", 0, 1)
    r2 = 1 - x2
    print("r2: ", r2)
    b = 1/r2
    # now find C3, assuming it also has y3 = 0
    r3 = 1 - r2
    c = 1/r3
    print("r3: ", r3)
    x3 = x2 - r2 - r3
    y3 = 0
    d = descartes(a, b, c)
    print(a, b, c, d)
    print("3: ", x3, y3)
    print("-------------")
    # A = bend*center = a*(x1+y1j)
    A = a*(x1+y1*1j)
    B = b*(x2+y2*1j)
    C = c*(x3+y3*1j)
    Dplus = (A + B + C) + 2*cmath.sqrt(A*B + A*C + B*C)
    Dminus = (A + B + C) - 2*cmath.sqrt(A*B + A*C + B*C)
    print(A)
    print(B)
    print(C)
    print(Dplus)
    print(Dminus)
    Dyplus = Dplus.imag/d
    Dyminus = Dminus.imag/d
    Dxplus = Dplus.real/d
    Dxminus = Dminus.real/d
    print("plus: dx = %.2f  dy = %.2f" % (Dxplus, Dyplus))
    print("minus: dx = %.2f  dy = %.2f" % (Dxminus, Dyminus))
    plot(a,b,c,d,A,B,C,Dplus,Dminus)


def plot(a,b,c,d,A,B,C,Dp,Dm):
    """plot the circles"""
    fig, ax = plt.subplots()
    patches = []
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.grid(True)

    for tup in [(a,A),(b,B),(c,C),(d,Dp),(d,Dm)]:
        x,y,radius = getData(tup)
        circle = Circle((x, y), radius)
        prealatches.append(circle)

    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)
    plt.show()


def getData(tup):
    """pull out x,y, radius"""
    bend, bendcenter = tup
    radius = 1/bend
    center = bendcenter/bend
    x = center.real
    y = center.imag
    return x, y, radius

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
    given a, b, c
    I set M and N (see below), and came up with this:
       d**2 + (-2N)d + (2M-N**2) = 0
    """
    M = a**2 + b**2 + c**2
    N = a + b + c
    # quadratic equation coefficients Ad**2 + Bd + C = 0
    A = 1
    B = -2*N
    C = (2*M) - (N**2)
    value = (B**2) - (4*A*C)
    epsilon = 1.0e-6
    if abs(value) < epsilon:
        value = 0
    print("value: ", value)
    try:
        sq = math.sqrt(value)
        root1 = (-1*B + sq)/(2*A)
        root2 = (-1*B - sq)/(2*A)
        print("root1: ", root1)
        print("root2: ", root2)
        return root2
    except ValueError:
        print("===========> verr")
        return 1


main()
