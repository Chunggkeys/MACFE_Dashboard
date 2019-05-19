from threading import Semaphore
from multiprocessing.connection import Client

resource = Semaphore(1)

## Data model to store state of vehicle
class guiModel:

    def __init__(self):
        
        self.speed = 0; self.batteryTemperature = 0
        self.bLevel = 0; self.shutdown = 0
        self.mTempOne = 0
        self.mTempTwo = 0; self.mTempThree = 0
        self.mTempFour = 0; self.maxPower = 0
        self.hv = 0; self.lv = 0
    
    ## Setters for guiModel state variables
    def setSpeed(self,speed):
        self.speed = speed
    
    def setBatteryLevel(self,batteryLevel):
        self.bLevel = batteryLevel

    def setBatteryTemperature(self,batteryTemperature):
        self.batteryTemperature = batteryTemperature
        
    def setShutdown(self,shutdown):
        self.shutdown = shutdown
    
    def setMotorTemperatureOne(self, motorTemperatureOne):
        self.mTempOne = motorTemperatureOne
        
    def setMotorTemperatureTwo(self,motorTemperatureTwo):
        self.mTempTwo = motorTemperatureTwo
    
    def setMotorTemperatureThree(self, motorTemperatureThree):
        self.mTempThree = motorTemperatureThree
    
    def setMotorTemperatureFour(self, motorTemperatureFour):
        self.mTempFour = motorTemperatureFour
    
    def setHV(self,hv):
        self.hv = hv
    
    def setLV(self,lv):
        self.lv = lv
    
    def setMaxPower(self,maxPower):
        self.maxPower = maxPower
    ##

    ## Getters for guiModel state variables
    def getSpeed(self):
        return str(self.speed)
	
    def getBatteryLevel(self):
        return str(self.bLevel)

    def getBatteryTemperature(self):
        return self.batteryTemperature

    def getMotorTemperatureOne(self):
        return self.mTempOne

    def getMotorTemperatureTwo(self):
        return self.mTempTwo

    def getMotorTemperatureThree(self):
        return self.mTempThree

    def getMotorTemperatureFour(self):
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
##

data = guiModel()

## Initializes the client, links to listener in presenter.py
address = ('localhost', 6000)    
client = Client(address, authkey=None)
##

## Methods to set and send data object    
def setSpeed(speed):
    data.setSpeed(speed)
    resource.acquire()
    client.send(data)
    resource.release()

def setBatteryLevel(batteryLevel):
    data.setBatteryLevel(batteryLevel)
    resource.acquire()
    client.send(data)
    resource.release()

def setBatteryTemperature(batteryTemperature):
    data.setBatteryTemperature(batteryTemperature)
    resource.acquire()
    client.send(data)
    resource.release()

def setMotorTemperatureOne(motorTemperatureOne):
    data.setMotorTemperatureOne(motorTemperatureOne)
    resource.acquire()
    client.send(data)
    resource.release()

def setMotorTemperatureTwo(motorTemperatureTwo):
    data.setMotorTemperatureTwo(motorTemperatureTwo)
    resource.acquire()
    client.send(data)
    resource.release()

def setMotorTemperatureThree(motorTemperatureThree):
    data.setMotorTemperatureThree(motorTemperatureThree)
    resource.acquire()
    client.send(data)
    resource.release()

def setMotorTemperatureFour(motorTemperatureFour):
    data.setMotorTemperatureFour(motorTemperatureFour)
    resource.acquire()
    client.send(data)
    resource.release()

def setShutdown(shutdown):
    data.setShutdown(shutdown)
    resource.acquire()
    client.send(data)
    resource.release()

def setMaxPower(maxPower):
    data.setMaxPower(maxPower)
    resource.acquire()
    client.send(data)
    resource.release()

def setHV(hv):
    data.setHV(hv)
    resource.acquire()
    client.send(data)
    resource.release()

def setLV(lv):
    data.setLV(lv)
    resource.acquire()
    client.send(data)
    resource.release()
##


    

    
    




