# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
puncta >> gui
"""
import numpy as np
import pathlib
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
from matplotlib.gridspec import GridSpec
import matplotlib as mpl

from . import FOV

# ==============================================================================
# controller
# ==============================================================================
class PunctaController(QtCore.QObject):

    indexChanged = QtCore.pyqtSignal(object)
    fileSelected = QtCore.pyqtSignal(object)
    fovLoaded = QtCore.pyqtSignal(object)
    cellSelected = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.fov = None
        self.index = None

        self.fileSelected.connect(self.open_image)
        self.cellSelected.connect(self.add_cell)

    def set_index(self, val):
        self.index = val
        self.indexChanged.emit(self.fov[self.index])

    def open_image(self, filename):
        self.fov = FOV.read_image(filename)
        self.fov.correct_background(show=False)
        self.fovLoaded.emit(self.fov)

    def add_cell(self, coords):
        self.fov.add_cell(coords)
        self.set_index(len(self.fov)-1)





# ==============================================================================
# plotting
# ==============================================================================
class FOVAxes(mpl.axes.Axes):
    name = "fov"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.axis('off')

    def plot(self, fov):
        self.imshow(fov.img, cmap="afmhot")

class CellAxes(mpl.axes.Axes):
    name = "cell"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.axis('off')

    def plot(self, cell):
        self.imshow(cell.img, cmap="afmhot")
        try:
            super().plot(*cell.punctum.get_draw_coords(), c='c')
        except AttributeError:
            pass

mpl.projections.register_projection(FOVAxes)
mpl.projections.register_projection(CellAxes)

class PunctaPickerCanvas(FigureCanvas):

    def __init__(self, controller):
        self.controller = controller
        self.fig = Figure()
        super().__init__(self.fig)
        self.fig.set_tight_layout(True)
        self.layout()
        self.connect()

    def layout(self):
        gs = GridSpec(1, 2)
        self.axFOV = self.fig.add_subplot(gs[0], projection="fov")
        self.axCell = self.fig.add_subplot(gs[1], projection="cell")

    def connect(self):
        self.controller.fovLoaded.connect(self.on_load_fov)
        self.controller.indexChanged.connect(self.on_change_cell)
        self.mpl_connect('button_release_event', self.on_release)

        rectProps = {"alpha": 0.5, "facecolor": "#E5FF00"}
        spanArgs = {"useblit": True, "button": 1, "rectprops": rectProps}
        self.zoomSpan = RectangleSelector(self.axFOV, self.on_zoom, **spanArgs)

    def on_load_fov(self, fov):
        self.axFOV.plot(fov)
        self.draw()

    def on_change_cell(self, cell):
        self.axCell.cla()
        self.axCell.plot(cell)
        self.draw()

    def on_zoom(self, evt1, evt2):
        self.controller.cellSelected.emit([int(evt1.xdata), int(evt2.xdata), int(evt1.ydata), int(evt2.ydata)])

    def on_release(self, evt):
        if evt.inaxes == self.axCell:
            print("cell")
        elif evt.inaxes == self.axFOV and evt.button == 3:
            print("reset")

# ==============================================================================
# widgets
# ==============================================================================
class OpenButton(QtWidgets.QPushButton):

    def __init__(self, controller, **kwargs):
        self.controller = controller
        super().__init__("Open File", **kwargs)
        self.clicked.connect(self.get_file)

    def get_file(self):
        fdArgs = {"caption":"Open Image",
                  "filter":"TIFF Image (*.tif)"}
        filename, filetype = QFileDialog.getOpenFileName(**fdArgs)
        # check that filename isn't null, then load and signal
        if filename:
            self.controller.fileSelected.emit(pathlib.Path(filename).absolute())


class CellSlider(QtWidgets.QSlider):

    def __init__(self, controller, **kwargs):
        self.controller = controller
        super().__init__(orientation=QtCore.Qt.Horizontal, **kwargs)


class CellIdLabel(QtWidgets.QLabel):
    lbl = "Cell ID: "

    def __init__(self, controller, **kwargs):
        self.controller = controller
        super().__init__(self.lbl, **kwargs)
        self.setMinimumWidth(200)


class FitButton(QtWidgets.QPushButton):

    def __init__(self, controller, **kwargs):
        self.controller = controller
        super().__init__("Find Punctum", **kwargs)
