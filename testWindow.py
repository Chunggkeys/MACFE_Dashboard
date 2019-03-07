from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys

class testWindow(QWidget):

    testSignal = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        #self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle("testWindow")

        self.button = QPushButton("Test", self)
        self.button.move(100,100)

        self.button.clicked.connect(self.test)

        self.show()
    
    def test(self):
        self.testSignal.emit()