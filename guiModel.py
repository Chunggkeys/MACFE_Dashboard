from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
import sys

class guiModel:

	#updateSignal = pyqtSignal()

	def __init__(self,mTemp,speed,bLevel,bTemp,mTorque,shutdown):
 		self.mTemp = mTemp; self.speed = speed 
 		self.bLevel = bLevel; self.shutdown = shutdown
 		self.bTemp = bTemp; self.mTorque = mTorque

	def setBatteryLevel(self, bLevel):
		self.bLevel = bLevel

	def setBatteryTemperature(self, bTemp):
		self.bTemp = bTemp

	def setMotorTemperature(self, mTemp):
		self.mTemp = mTemp
	
	def setSpeed(self, speed):
		self.speed = speed
	
	def setMotorTorque(self, mTorque):
		self.mTorque = mTorque
	
	def setShutdown(self, shutdown):
		self.shutdown = shutdown

	def getMotorTemperature(self):
		return str(self.mTemp)
	
	def getSpeed(self):
		return str(self.speed)
	
	def getBatteryLevel(self):
		return str(self.bLevel)

	def getBatteryTemperature(self):
		return str(self.bTemp)

	def getMotorTorque(self):
		return self.mTorque
	
	def getShutdown(self):
		return self.shutdown