from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
patches = []
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.grid(True)

x1 = 0.5
y1 = 0.2
r = 0.1
circle = Circle((x1, y1), r)
patches.append(circle)
x1 = 0.6
y1 = 0.2
r = 0.4
circle = Circle((x1, y1), r)
patches.append(circle)

p = PatchCollection(patches, alpha=0.4)
ax.add_collection(p)

plt.show()
