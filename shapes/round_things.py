# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
shapes >> round_things
"""

import numpy as np
import matplotlib.pyplot as plt

from shapes import Shape

__all__ = ["Circle"]

class Circle(Shape):

    def __init__(self, x=0, y=0, r=1):
        super().__init__(x=x, y=y)
        self._r = r

    @property
    def r(self):
        return self._r
    @r.setter
    def r(self, val):
        try:
            if val > 0:
                self._r = val
        except TypeError:
            print("invalid type, attribute not updated")

    @property
    def D(self):
        return 2*self.r

    @property
    def C(self):
        return 2*np.pi*self.r

    def get_area(self):
        return np.pi * self.r**2

    def get_draw_coords(self):
        t = np.linspace(0, 2*np.pi, 360)
        x = self.x + self.r*np.cos(t)
        y = self.y + self.r*np.sin(t)
        return x, y
