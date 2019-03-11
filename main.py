from presenter import Presenter
from view import *
from guiModel import guiModel
from PyQt5 import QtWidgets
from test import *
import sys

def main():

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    gModel = guiModel(0,0,1232,0,0,0,0,0,0)
    select = selectWindow()
    MWindowNoSpeed = MainWindowNoSpeed()
    MWindowSpeed = MainWindowSpeed()
    p = Presenter(select, MWindowNoSpeed, MWindowSpeed, gModel)

    ## Accepts signals from View module and opens respective GUIs
    select.yesClicked.connect(p.withSpeed)
    select.noClicked.connect(p.withNoSpeed)
    ##
    
    sys.exit(app.exec_())


main()
    