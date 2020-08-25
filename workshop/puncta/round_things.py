# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
shapes >> round_things
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

__all__ = ["Circle"]


class Shape():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate(self, dx=0, dy=0):
        self.x += dx
        self.y += dy


class Circle(Shape):

    def __init__(self, x=0, y=0, r=1):
        super().__init__(x=x, y=y)
        self._r = r

    def magnify(self, dr):
        self.r = self.r*dr

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

    def fit_to_gaussian(self, img):
        x = np.arange(img.shape[0])
        y = np.arange(img.shape[1])
        XX, YY = np.meshgrid(x, y)

        coord = np.vstack([XX.ravel(), YY.ravel()])
        beta, _ = curve_fit(gau2d_circle, coord, img.ravel())
        self.x = beta[1]
        self.y = beta[2]
        self.r = np.abs(beta[3])*1.5




def gau2d(XX, A, muX, muY, sigX, sigY):
    xX = (XX[0]-muX)**2
    yX = (XX[1]-muY)**2
    expPart = xX/(2*sigX**2) + yX/(2*sigY**2)
    return A * np.exp(-expPart)

def gau2d_circle(XX, A, muX, muY, sig):
    return gau2d(XX, A, muX, muY, sig, sig)
