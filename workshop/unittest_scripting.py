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
print(f)

f.correct_background(show=True)
# f.threshhold()

f.add_cell([656, 693, 641, 676])
c = f[0]
c.add_punctum([28, 26])

f.add_cell([560, 585, 486, 518])
f[1].add_punctum([9, 7], isTesting=False)
f.add_cell([964, 994, 251, 271])
f[2].add_punctum([9, 12], isTesting=False)
print(f)
