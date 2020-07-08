# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
shapes >> not_round_things
"""

import numpy as np
import matplotlib.pyplot as plt

from shapes import Shape


__all__ = ["Square", "Rectangle"]


class Square(Shape):

    def __init__(self, x, y, w):
        super().__init__(x=x, y=y)
        self._w = w

    @property
    def w(self):
        return self._w
    @w.setter
    def w(self, val):
        try:
            if val > 0:
                self._w = val
        except TypeError:
            print("invalid type, attribute not updated")

    @property
    def h(self):
        return self.w

    def get_area(self):
        return self.w * self.h

    def get_draw_coords(self):
        xMin, xMax = self.x + (np.array([-1, 1]) * (self.w/2))
        yMin, yMax = self.y + (np.array([-1, 1]) * (self.h/2))

        N = 100
        xRange = np.linspace(xMin, xMax, N)
        yRange = np.linspace(yMin, yMax, N)

        leftVert = np.vstack((np.ones(N)*xMin, yRange)).T
        topHorz = np.vstack((xRange, np.ones(N)*yMax)).T
        rightVert = np.vstack((np.ones(N)*xMax, yRange[::-1])).T
        botHorz = np.vstack((xRange[::-1], np.ones(N)*yMin)).T
        x, y = np.vstack((leftVert, topHorz, rightVert, botHorz)).T
        return x, y


class Rectangle(Square):

    def __init__(self, x, y, w, h):
        super().__init__(x=x, y=y, w=w)
        self._h = h

    @property
    def h(self):
        return self._h
    @h.setter
    def h(self, val):
        try:
            if val > 0:
                self._h = val
        except TypeError:
            print("invalid type, attribute not updated")
