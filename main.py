from presenter import Presenter
from view import *
from guiModel import guiModel
from PyQt5 import QtWidgets
from test import *
import sys

def main():

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    gModel = guiModel(0,0,0,0,0,0,0,0,0,0,0)
    MWindow= MainWindow()
    p = Presenter(MWindow,gModel)

    p.open()
    
    sys.exit(app.exec_())


main()
    