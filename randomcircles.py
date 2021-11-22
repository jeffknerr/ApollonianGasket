"""
random circles using matplotlib and numpy
"""

import numpy as np
from numpy.random import default_rng
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
patches = []
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.grid(True)
ax.set_aspect(1)
ax.set_title("random circles")
ax.set_xlabel("x")
ax.set_ylabel("y")

N = 50
seed = 42
scale = 0.4
# pick N random radii
# pick N random xs
# pick N random ys
# make N Circle objects, add patch collection to axes
radii = default_rng(seed).random((N))*scale
xs = (2*default_rng().random((N))) - 1   # from -1 to 1
ys = (2*default_rng().random((N))) - 1
circles = [Circle((xs[i],ys[i]), radii[i]) for i in range(N)]
colors = ["red","green","blue","yellow","pink","orange"]
p = PatchCollection(circles, alpha=0.4, edgecolor="black", facecolor=colors)
ax.add_collection(p)

plt.show()
