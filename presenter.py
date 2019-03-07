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
from testWindow import *
from view import *


class Presenter:

    #update = pyqtSignal(tuple)

    def __init__(self, selectWindow, MainWindowNoSpeed, MainWindowSpeed, guiModel):
        self._selectWindow = selectWindow
        self._mainWindowSpeed = MainWindowSpeed
        self._guiModel = guiModel
        self._mainWindowNoSpeed = MainWindowNoSpeed 
    
    def withSpeed(self):
        self._mainWindowSpeed.show()
        self.test = Test(self._guiModel)
        #self._guiModel.updateSignal.connect(self.getRequest)
        self.test.updateSignal.connect(self.getRequest)
        #self.testWindow = testWindow()
        #self.testWindow.testSignal.connect(self.getRequest)
    
    def withNoSpeed(self):
        self._mainWindowNoSpeed.show()
        self.test = Test(self._guiModel)
        #self._guiModel.updateSignal.connect(self.getRequest)
        self.test.updateSignal.connect(self.getRequest)
        #self.testWindow = testWindow()
        #self.testWindow.testSignal.connect(self.getRequest)
       
    def changeVal(self,displayValues):

        self._mainWindowNoSpeed.processValues(displayValues)
        self._mainWindowSpeed.processValues(displayValues)

    def getRequest(self, values): ##Tester Request
        print("hi")
        #self.test.updateSignal.connect(self.processValues)
        
        #self._guiModel.updateSignal.connect(self.processValues) 
        # self.values = t.test()
        self.processValues(values)
    
    def processValues(self, values):
        self.values = values

        displayValues = []
        
        for i in range(6):
            displayValues.append(self.values[i])
            
        self.updateValues(displayValues)
        
    def updateValues(self, displayValues):
        # self._guiModel.setMotorTemperature(float(self.values[0]))
        # self._guiModel.setSpeed(float(self.values[1]))
        # self._guiModel.setBatteryLevel(float(self.values[2]))
        # self._guiModel.setBatteryTemperature(float(self.values[3]))
        # self._guiModel.setMotorTorque(float(self.values[4]))
        # self._guiModel.setShutdown(float(self.values[5]))
        self.changeVal(displayValues)

    #def getRequest(self): ##Real values from CAN   
        ## read CAN values
        