from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QObject
import sys

class guiModel(QObject):

	updateSignal = pyqtSignal(list)

	def __init__(self,speed,bLevel,bTemp,mTempOne,mTempTwo,mTempThree,mTempFour,shutdown,maxPower,hv,lv):

		super().__init__()
		#self.listValues = []
		self.speed = speed 
		self.bLevel = bLevel; self.shutdown = shutdown
		self.bTemp = bTemp; self.mTempOne = mTempOne
		self.mTempTwo = mTempTwo; self.mTempThree = mTempThree
		self.mTempFour = mTempFour; self.maxPower = maxPower
		self.hv = hv; self.lv = lv

	## Setters for car info
	def setBatteryLevel(self, bLevel):
		self.bLevel = bLevel

	def setBatteryTemperature(self, bTemp):
		self.bTemp = bTemp

	def setMotorTemperature(self, mTemp):
		self.mTemp = mTemp
	
	def setSpeed(self, speed):
		self.speed = speed
		
	def setMotorTempOne(self, mTorqueOne):
		self.mTempOne = mTorqueOne
	
	def setMotorTempTwo(self, mTorqueTwo):
		self.mTempTwo = mTorqueTwo
	
	def setMotorTempThree(self, mTorqueThree):
		self.mTempThree = mTorqueThree
	
	def setMotorTempFour(self, mTorqueFour):
		self.mTempFour = mTorqueFour
		
	def setShutdown(self, shutdown):
		self.shutdown = shutdown
		
	def sefMaxPower(self, maxPower):
		self.maxPower = maxPower
	
	def setHV(self, hv):
		self.hv = hv
	
	def setLV(self, lv):
		self.lv = lv
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

	def getMotorTempOne(self):
		return self.mTempOne

	def getMotorTempTwo(self):
		return self.mTempTwo

	def getMotorTempThree(self):
		return self.mTempThree

	def getMotorTempFour(self):
		return self.mTempFour
		
	def getShutdown(self):
		return self.shutdown
	
	def getMaxPower(self):
		return self.maxPower
	
	def getHV(self):
		return self.hv
	
	def getLV(self):
		return self.lv
	##