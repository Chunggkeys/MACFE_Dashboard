#Grabs data from source, passes data to Presenter through presenter.getRequest
#mTemp, speed, bLevel, bTemp
##Use pyqtSignal to emit every time deteched value change
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from guiModel import *
import sys

import csv

# def test():

#     with open("testFiles/sampleValues.csv", newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        
#         for row in spamreader:
#             motorTemperature = row[0]
#             speed = row[1]
#             batteryLevel = row[2]
#             batteryTemperature = row[3]
#             motorTorque = row[4]
#             shutdown = row[5]

    
#     return [motorTemperature, speed, batteryLevel, batteryTemperature, motorTorque, shutdown]

class Test(QThread):

	updateSignal = pyqtSignal(list)

	def __init__(self, guiModel):
		self._guiModel = guiModel
		super().__init__()
		self.start()
	
	def run(self):
		
		while self.isRunning:
			spam = sys.stdin.readline()
			values = spam.split(",")
			motorTemperature = values[0]
			self._guiModel.setMotorTemperature(motorTemperature)
			speed = values[1]
			self._guiModel.setSpeed(speed)
			batteryLevel = values[2]
			self._guiModel.setBatteryLevel(batteryLevel)
			batteryTemperature = values[3]
			self._guiModel.setBatteryTemperature(batteryTemperature)
			motorTorque = values[4]
			self._guiModel.setMotorTorque(motorTorque)
			shutdown = values[5]
			self._guiModel.setShutdown(shutdown)

			self.updateSignal.emit(values)

	# def stop(self):
	# 	self.isRunning = False