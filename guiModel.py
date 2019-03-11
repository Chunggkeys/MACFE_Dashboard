from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QObject
import sys

class guiModel(QObject):

	updateSignal = pyqtSignal(list)

	def __init__(self,mTemp,speed,bLevel,bTemp,mTempOne,mTempTwo,mTempThree,mTempFour,shutdown):

		super().__init__()
		#self.listValues = []
		self.mTemp = mTemp; self.speed = speed 
		self.bLevel = bLevel; self.shutdown = shutdown
		self.bTemp = bTemp; self.mTempOne = mTempOne
		self.mTempTwo = mTempTwo; self.mTempThree = mTempThree
		self.mTempFour = mTempFour

	## Setters for car info
	def setBatteryLevel(self, bLevel):
		self.bLevel = bLevel
		#self.listValues.append(self.bLevel)

	def setBatteryTemperature(self, bTemp):
		self.bTemp = bTemp
		#self.listValues.append(self.bTemp)

	def setMotorTemperature(self, mTemp):
		self.mTemp = mTemp
		#self.listValues.append(self.mTemp)
	
	def setSpeed(self, speed):
		self.speed = speed
		#self.listValues.append(self.speed)
		
	def setMotorTorqueOne(self, mTorqueOne):
		self.mTempOne = mTorqueOne
		#self.listValues.append(self.mTorque)
	
	def setMotorTorqueTwo(self, mTorqueTwo):
		self.mTempTwo = mTorqueTwo
	
	def setMotorTorqueThree(self, mTorqueThree):
		self.mTempThree = mTorqueThree
	
	def setMotorTorqueFour(self, mTorqueFour):
		self.mTempFour = mTorqueFour
		
	def setShutdown(self, shutdown):
		self.shutdown = shutdown
		#self.listValues.append(self.shutdown)
		#self.updateSignal.emit(self.listValues)
	##

	## getters for car info
	def getMotorTemperature(self):
		return str(self.mTemp)
	
	def getSpeed(self):
		return str(self.speed)
	
	def getBatteryLevel(self):
		return str(self.bLevel)

	def getBatteryTemperature(self):
		return str(self.bTemp)

	def getMotorTorqueOne(self):
		return self.mTempOne

	def getMotorTorqueTwo(self):
		return self.mTempTwo

	def getMotorTorqueThree(self):
		return self.mTempThree

	def getMotorTorqueFour(self):
		return self.mTempFour
		
	def getShutdown(self):
		return self.shutdown
	##