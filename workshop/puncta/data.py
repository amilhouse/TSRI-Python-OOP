# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
puncta >> data
"""
import numpy as np
from scipy import ndimage
from datetime import datetime
import h5py, json

from skimage import io, filters
from skimage import img_as_float
from skimage.morphology import reconstruction

import matplotlib.pyplot as plt

from . import Circle

class FOV():

    def __init__(self, img, corrImg=None, id_=None, cells=None):
        if id_ is None:
            self._id = hex(int(datetime.now().timestamp()))
        else:
            self._id = id_
        self._img = img
        if corrImg is None:
            self.img = img
        else:
            self.img = corrImg
        # self._regions = None
        if cells is None:
            self._cells = []
        else:
            self._cells = cells

    def __getitem__(self, index):
        return self._cells[index]

    def __len__(self):
        return len(self._cells)

    def __str__(self):
        return f"Field of View {self._id}\t[{len(self)} selected cells]"

    def add_cell(self, coords):
        self._cells.append(Cell(self, coords))
        print("added ", self[-1])

    @classmethod
    def read_image(cls, filename):
        img = io.imread(filename, as_gray=True)
        id_ = hex(int(datetime.now().timestamp()))
        return cls(img, id_)

    @classmethod
    def load(cls, filename):
        with h5py.File(filename, "r") as HF:
            id_ = HF.attrs["id"]
            data = HF["FOV"]
            corrImg = data[:,:,0]
            img = data[:,:,1]
            fov = cls(img, corrImg=corrImg, id_=id_, cells=None)
            cells = []
            for key, item in HF["cells"].attrs.items():
                cells.append(Cell.from_json(fov, key, item))
            fov._cells = cells
            return fov

    def save(self, filename):
        with h5py.File(filename, "w") as HF:
            HF.attrs["id"] = self._id
            data = np.stack((self.img, self._img), axis=2)
            HF.create_dataset("FOV", data=data, compression="gzip")
            group = HF.create_group("cells")
            for cell in self:
                group.attrs[str(cell._id)] = cell.as_json()

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
            ax1.imshow(self._img, cmap="afmhot")
            ax1.set_title('Original')
            ax1.axis('off')
            ax2 = plt.subplot(1, 2, 2, sharex=ax1, sharey=ax1)
            ax2.imshow(self.img, cmap="afmhot")
            ax2.set_title('Background-Corrected')
            ax2.axis('off')
            plt.show()

    # def threshhold(self, show=False):
    #     """ https://bit.ly/2FUW3eI """
    #     thresholds = filters.threshold_multiotsu(self.img, classes=3)
    #     self._regions = np.digitize(self.img, bins=thresholds)
    #
    #     if show:
    #         ax1 = plt.subplot(1, 2, 1)
    #         ax1.imshow(self.img, cmap="bone")
    #         ax1.set_title('Original')
    #         ax1.axis('off')
    #         ax2 = plt.subplot(1, 2, 2, sharex=ax1, sharey=ax1)
    #         ax2.imshow(self._regions, cmap="bone")
    #         ax2.set_title('Multi-Otsu thresholding')
    #         ax2.axis('off')
    #         plt.show()



class Cell():

    def __init__(self, parent, coords, id_=None, punctum=None):
        self._parent = parent
        if id_ is None:
            self._id = f"{parent._id}:{len(parent):03d}"
        else:
            self._id = id_
        self._coords = coords
        self.punctum = punctum

    def as_json(self):
        try:
            p = self.punctum.as_json()
        except AttributeError:
            p = None

        return json.dumps({"id": str(self._id),
                           "coords": self._coords,
                           "punctum": p})

    def __str__(self):
        return f"Cell {self._id}"

    @classmethod
    def from_json(cls, parent, key, data):
        d = json.loads(data)
        p = d["punctum"]
        if p is not None:
            p = Circle.from_json(p)
        return cls(parent, d["coords"], d["id"], p)

    @property
    def img(self):
        y1, y2, x1, x2 = self._coords
        return self._parent.img[x1:x2, y1:y2]

    def add_punctum(self, initCoords, r=2):
        x, y = initCoords
        self.punctum = Circle(x, y, r=r)

    def fit_punctum(self, show=False, isTesting=True):
        if isTesting:
            plt.imshow(self.img, cmap="afmhot")
            plt.show()
        # upsample image
        img0 = ndimage.zoom(self.img, 3.0)
        if isTesting:
            plt.imshow(img0, cmap="afmhot")
            plt.show()
        # crop upsampled image near initial point
        # initCoords = np.array(initCoords, dtype=np.int)*3
        initCoords = np.array([self.punctum.x, self.punctum.y], dtype=np.int)*3
        r = self.punctum.r
        ylim = slice(initCoords[0]-20, initCoords[0]+20)
        xlim = slice(initCoords[1]-20, initCoords[1]+20)
        i = img0[xlim, ylim]
        if isTesting:
            plt.imshow(i, cmap="afmhot")
            plt.show()
        # instantiate circle object at center of cropped image
        x, y = i.shape
        p = Circle(x/2, y/2, r=r*3.0)
        if isTesting:
            plt.imshow(i, cmap="afmhot")
            plt.plot(*p.get_draw_coords(), c='c')
            plt.show()
        # find optimal circle parameters
        p.fit_to_gaussian(i)
        if isTesting:
            plt.imshow(i, cmap="afmhot")
            plt.plot(*p.get_draw_coords(), c='c')
            plt.show()
        # transform back to original coordinates of resampled image
        y0, x0 = img0.shape
        p.x = initCoords[0]-20+p.x
        p.y = initCoords[1]-20+p.y
        if isTesting:
            plt.imshow(img0, cmap="afmhot")
            plt.plot(*p.get_draw_coords(), c='c')
            plt.show()
        # transform back to original coordinates
        p.x = p.x/3
        p.y = p.y/3
        p.r = p.r/3
        if isTesting:
            plt.imshow(self.img, cmap="afmhot")
            plt.plot(*p.get_draw_coords(), c='c')
            plt.show()
        self.punctum = p
