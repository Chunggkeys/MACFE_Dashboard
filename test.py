#Grabs data from source, passes data to Presenter through presenter.getRequest
#mTemp, speed, bLevel, bTemp
##Use pyqtSignal to emit every time deteched value change
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
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

	def __init__(self):
		super().__init__()
		self.start()
	
	def run(self):
		
		while self.isRunning:
			spam = sys.stdin.readline()
			values = spam.split(",")
			motorTemperature = values[0]
			speed = values[1]
			batteryLevel = values[2]
			batteryTemperature = values[3]
			motorTorque = values[4]
			shutdown = values[5]

			self.updateSignal.emit(values)

	# def stop(self):
	# 	self.isRunning = False