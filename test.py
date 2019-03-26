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

	updateTestSignal = pyqtSignal(list)

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
			speed = values[0]
			self._guiModel.setSpeed(speed)

			batteryLevel = int(values[1])
			self._guiModel.setBatteryLevel(batteryLevel)

			batteryTemperature = int(values[2])
			self._guiModel.setBatteryTemperature(batteryTemperature)

			motorTorqueOne = int(values[3])
			self._guiModel.setMotorTempOne(motorTorqueOne)

			motorTorqueTwo = int(values[4])
			self._guiModel.setMotorTempTwo(motorTorqueTwo)

			motorTorqueThree = int(values[5])
			self._guiModel.setMotorTempThree(motorTorqueThree)

			motorTorqueFour = int(values[6])
			self._guiModel.setMotorTempFour(motorTorqueFour)

			shutdown = int(values[7])
			self._guiModel.setShutdown(shutdown)

			maxPower = int(values[8])
			self._guiModel.setMaxPower(maxPower)

			hv = int(values[9])
			self._guiModel.setHV(hv)
			
			lv = int(values[10])
			self._guiModel.setLV(lv)

			## Emits a signal, telling presenter.py that values have been changed
			self.updateTestSignal.emit(values)
			##

		##
	##

##