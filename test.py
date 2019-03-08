#Grabs data from source, passes data to Presenter through presenter.getRequest
#mTemp, speed, bLevel, bTemp
##Use pyqtSignal to emit every time deteched value change
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from guiModel import *
import sys

## Test class
class Test(QThread):

	updateSignal = pyqtSignal(list)

	def __init__(self, guiModel):

		self._guiModel = guiModel
		
		## Initializes parent class, which is QThread
		super().__init__()
		##

		self.start()
	
	## Runs thread until appliation close
	def run(self):
		
		## Consistently waits for input, and updates variables in guiModel
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

			## Emits a signal, telling presenter.py that values have been changed
			self.updateSignal.emit(values)
			##

		##
	##

##