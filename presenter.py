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
    def __init__(self, selectWindow, MainWindowNoSpeed, guiModel):
        self._selectWindow = selectWindow
        #self._mainWindowSpeed = MainWindowSpeed
        self._guiModel = guiModel
        self._mainWindowNoSpeed = MainWindowNoSpeed 
    
    ## Opens GUI with speed indicator window and initializes Test/CAN module
    # def withSpeed(self):
    #     self._mainWindowSpeed.show()
    #     self.test = Test(self._guiModel)

    #     ## Accepts signal from Test module
    #     self.test.updateTestSignal.connect(self.processValues)
        ##

    ##
       
    ## Opens GUI without speed indicator window and initializes Test/CAN module
    def open(self):
        self._mainWindowNoSpeed.show()
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
        
        self._mainWindowNoSpeed.processValues(self.values)
        # self._mainWindowSpeed.processValues(displayValues)
    ##

    #def updateCANValues(self): ##Real values from CAN   
        ## read CAN values
        