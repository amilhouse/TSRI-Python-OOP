# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
puncta picker app
"""
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore, QtGui
import sys

class PunctaPickerApp(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__(windowTitle="Puncta Picker")
        self.resize(1000, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    win = PunctaPickerApp()
    win.show()
    sys.exit(app.exec_())
