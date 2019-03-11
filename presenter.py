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
    def __init__(self, selectWindow, MainWindowNoSpeed, MainWindowSpeed, guiModel):
        self._selectWindow = selectWindow
        self._mainWindowSpeed = MainWindowSpeed
        self._guiModel = guiModel
        self._mainWindowNoSpeed = MainWindowNoSpeed 
    
    ## Opens GUI with speed indicator window and initializes Test/CAN module
    def withSpeed(self):
        self._mainWindowSpeed.show()
        self.test = Test(self._guiModel)

        ## Accepts signal from Test module
        self.test.updateTestSignal.connect(self.processValues)
        #

    ##
       
    ## Opens GUI without speed indicator window and initializes Test/CAN module
    def withNoSpeed(self):
        self._mainWindowNoSpeed.show()
        self.test = Test(self._guiModel)

        ## Accepts signal from Test module
        self.test.updateTestSignal.connect(self.processValues)
        ##

    ##
    
    ## Creates auxiliary list and passes that list to function that displays
    def processValues(self, values):
        self.values = values

        displayValues = []
        length = len(values)
        
        for i in range(length):
            displayValues.append(self.values[i])
            
        self.updateValues(displayValues)
    ##

    ##  Changes values in respective GUI
    def updateValues(self, displayValues):
        
        self._mainWindowNoSpeed.processValues(displayValues)
        self._mainWindowSpeed.processValues(displayValues)
    ##

    #def getRequest(self): ##Real values from CAN   
        ## read CAN values
        