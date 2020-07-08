# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
package: shapes
"""

class Shape():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate(self, dx=0, dy=0):
        self.x += dx
        self.y += dy



import shapes.graphics
from shapes.round_things import *
from shapes.not_round_things import *
