# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
script: try shapes package
"""

import matplotlib.pyplot as plt
import shapes

# ==============================================================================
c1 = shapes.Circle(0,0,1)
ax = plt.subplot(1, 1, 1, aspect="equal", projection="shape")
ax.plot_shape(c1)
c1b = c1
c1b.translate(2,2)
ax.plot_shape(c1)

plt.show()

# ==============================================================================
shapesList = [c1]
shapesList.append(shapes.Circle(5,5,3))
shapesList.append(shapes.Square(0,0,2))
shapesList.append(shapes.Square(-5,-5,7))
shapesList.append(shapes.Rectangle(0,0,2,3.14))
shapesList.append(shapes.Rectangle(5,-5,3.14,6))

ax = plt.subplot(1, 1, 1, aspect="equal", projection="shape")
for sh in shapesList:
    ax.plot_shape(sh)
plt.show()
