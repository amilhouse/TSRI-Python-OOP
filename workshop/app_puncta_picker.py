# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
puncta picker app
"""
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore, QtGui
import sys

from puncta import gui

class PunctaPickerApp(QtWidgets.QMainWindow):

    def __init__(self):
        self.controller = gui.PunctaController()
        super().__init__(windowTitle="Puncta Picker")
        self.resize(1000, 600)
        self.layout()

    def layout(self):
        pnl = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout()
        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()

        hbox1.addWidget(gui.PunctaPickerCanvas(self.controller))

        hbox2.addWidget(gui.OpenButton(self.controller))
        hbox2.addWidget(gui.CellSlider(self.controller), stretch=1)
        hbox2.addWidget(gui.CellIdLabel(self.controller))
        hbox2.addWidget(gui.FitButton(self.controller))

        vbox.addLayout(hbox1, stretch=1)
        vbox.addLayout(hbox2)
        pnl.setLayout(vbox)
        self.setCentralWidget(pnl)


if __name__ == '__main__':
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    win = PunctaPickerApp()
    win.show()
    sys.exit(app.exec_())
