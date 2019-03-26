######################################## INFO #######################################
#																					
#	presenter.py will take info from the Raspberry Pi and will process any data 	
#	necessary to manipulate the dashboard GUI									
#																					
#####################################################################################

#import test as t
from test import *
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QPalette
from PyQt5.QtCore import *
from guiModel import guiModel
from view import *


class Presenter:

    ## Initializes the presenter with instances of the GUI with/without speed indication, and model 
    def __init__(self, MainWindow, guiModel):
        self._guiModel = guiModel
        self._mainWindow = MainWindow 
    
    
    ## Opens GUI and initializes Test/CAN module
    def open(self):
        self._mainWindow.show()
        self.test = Test(self._guiModel)

        ## Accepts signal from Test module
        self.test.updateTestSignal.connect(self.updateTestValues)
        ##
    ##

    ##  Changes values in respective GUI
    def updateTestValues(self, values):

        self.values = []
        size = len(values)

        for i in range(size):
            self.values.append(int(values[i]))
        
        self._mainWindow.processValues(self.values)
        
    ##

    #def updateCANValues(self): ##Real values from CAN   
        ## read CAN values
        