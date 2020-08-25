# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
puncta unittest => scripting
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from puncta import FOV

filename = Path("./sample_image.tif")
f = FOV.read_image(filename)

f.correct_background()
f.threshhold()

f.add_cell([656, 693, 641, 676])
c = f[0]
c.add_punctum([28, 26])
