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

    fileSelected = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.fov = None

        self.fileSelected.connect(self.open_image)

    def open_image(self, filename):
        self.fov = FOV.read_image(filename)
        print(self.fov)




# ==============================================================================
# plotting
# ==============================================================================
class FOVAxes(mpl.axes.Axes):
    name = "fov"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.axis('off')

class CellAxes(mpl.axes.Axes):
    name = "cell"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.axis('off')

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
        self.mpl_connect('button_release_event', self.on_release)

        rectProps = {"alpha": 0.5, "facecolor": "#E5FF00"}
        spanArgs = {"useblit": True, "button": 1, "rectprops": rectProps}
        self.zoomSpan = RectangleSelector(self.axFOV, self.on_zoom, **spanArgs)

    def on_zoom(self, eclick, erelease):
        # "eclick and erelease are matplotlib events at press and release."
        # print('startposition: (%f, %f)' % (eclick.xdata, eclick.ydata))
        # print('endposition  : (%f, %f)' % (erelease.xdata, erelease.ydata))
        pass

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
