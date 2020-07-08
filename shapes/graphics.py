# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
shapes >> graphics
"""

import matplotlib as mpl


gray = "#bbbbbb"

class ShapeAxes(mpl.axes.Axes):
    name = "shape"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def plot_shape(self, s, **kwargs):
        self.set_xlim(-10, 10)
        self.set_ylim(-10, 10)
        self.axhline(0, c=gray, lw=0.5, ls=":")
        self.axvline(0, c=gray, lw=0.5, ls=":")

        super().plot(*s.get_draw_coords(), **kwargs)



mpl.projections.register_projection(ShapeAxes)
