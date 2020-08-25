# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
puncta >> data
"""
import numpy as np
from scipy import ndimage

from skimage import io, filters
# from scipy.ndimage import gaussian_filter
from skimage import img_as_float
from skimage.morphology import reconstruction

import matplotlib.pyplot as plt

from . import Circle

class FOV():

    def __init__(self, img):
        self._img = img
        self.img = img
        self._regions = None
        self._cells = []

    def __getitem__(self, index):
        return self._cells[index]

    def __len__(self):
        return len(self._cells)

    def add_cell(self, coords):
        self._cells.append(Cell(self, coords))

    @classmethod
    def read_image(cls, filename):
        img = io.imread(filename, as_gray=True)
        return cls(img)

    def correct_background(self, show=False):
        """ https://bit.ly/3li6ity """
        image = img_as_float(self._img)
        image = ndimage.gaussian_filter(image, 1)
        seed = np.copy(image)
        seed[1:-1, 1:-1] = image.min()
        mask = image
        dilated = reconstruction(seed, mask, method='dilation')
        self.img = image - dilated

        if show:
            ax1 = plt.subplot(1, 2, 1)
            ax1.imshow(self._img, cmap="bone")
            ax1.set_title('Original')
            ax1.axis('off')
            ax2 = plt.subplot(1, 2, 2, sharex=ax1, sharey=ax1)
            ax2.imshow(self.img, cmap="bone")
            ax2.set_title('Background-Corrected')
            ax2.axis('off')
            plt.show()

    def threshhold(self, show=False):
        """ https://bit.ly/2FUW3eI """
        thresholds = filters.threshold_multiotsu(self.img, classes=3)
        self._regions = np.digitize(self.img, bins=thresholds)

        if show:
            ax1 = plt.subplot(1, 2, 1)
            ax1.imshow(self.img, cmap="bone")
            ax1.set_title('Original')
            ax1.axis('off')
            ax2 = plt.subplot(1, 2, 2, sharex=ax1, sharey=ax1)
            ax2.imshow(self._regions, cmap="bone")
            ax2.set_title('Multi-Otsu thresholding')
            ax2.axis('off')
            plt.show()



class Cell():

    def __init__(self, parent, coords):
        self._parent = parent
        self._coords = coords
        self.punctum = None

    @property
    def img(self):
        y1, y2, x1, x2 = self._coords
        return self._parent.img[x1:x2, y1:y2]

    def add_punctum(self, initCoords, r=2, show=False, isTesting=True):
        # upsample image
        img0 = ndimage.zoom(self.img, 3.0)
        # crop upsampled image near initial point
        initCoords = np.array(initCoords, dtype=np.int)*3
        ylim = slice(initCoords[0]-20, initCoords[0]+20)
        xlim = slice(initCoords[1]-20, initCoords[1]+20)
        i = img0[xlim, ylim]
        if isTesting:
            plt.imshow(i, cmap="bone")
            plt.show()
        # instantiate circle object at center of cropped image
        x, y = i.shape
        p = Circle(x/2, y/2, r=r*3.0)
        if isTesting:
            plt.imshow(i, cmap="bone")
            plt.plot(*p.get_draw_coords(), c='r')
            plt.show()
        # find optimal circle parameters
        p.fit_to_gaussian(i)
        if isTesting:
            plt.imshow(i, cmap="bone")
            plt.plot(*p.get_draw_coords(), c='r')
            plt.show()
        # transform back to original coordinates of resampled image
        y0, x0 = img0.shape
        p.x = initCoords[0]-20+p.x
        p.y = initCoords[1]-20+p.y
        if isTesting:
            plt.imshow(img0, cmap="bone")
            plt.plot(*p.get_draw_coords(), c='r')
            plt.show()
        # transform back to original coordinates
        p.x = p.x/3
        p.y = p.y/3
        p.r = p.r/3
        if isTesting:
            plt.imshow(self.img, cmap="bone")
            plt.plot(*p.get_draw_coords(), c='r')
            plt.show()
        self.punctum = p
