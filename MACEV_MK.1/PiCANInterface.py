#!/usr/bin/python3
#
# simple_rx_test.py
# 
# This is simple CAN receive python program. All messages received are printed out on screen.
# For use with PiCAN boards on the Raspberry Pi
# http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-2-p-1475.html
#
# Make sure Python-CAN is installed first http://skpang.co.uk/blog/archives/1220
#
# 01-02-16 SK Pang
#
#
#

import can
import time
import guiModel as gm
import os
import serial

print('\n\rCAN Rx test')
print('Bring up CAN0....')
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
temperatureID = 502; vehicleID = 503
filter = [{"can_id": 0x502, "can_mask": 0x7FF, "extended": False},{"can_id": 0x503, "can_mask": 0x7FF, "extended": False}]

port = "/dev/ttyS0"
ser = serial.Serial(port, baudrate=57600, timeout=0.5)

try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
	bus.set_filters(filter)
except OSError:
	print('Cannot find PiCAN board.')
	exit()
	
print('Ready')
prevTime = 0;

def parseSpeed(data):
    try:
        data = data.decode().split(",")
        if data[0] == "$GPRMC":
            if data[2] == 'V':
                print("No satellite")
                return
            
            print("Parsing Speed value")

            tempSpeed = data[7]
            speed = tempSpeed * 1.852
    
    except UnicodeDecodeError:
        print("Exception")
        return
    
    return speed

try:
    while True:
        ## gpsparse
        data = ser.readline()
        sendSpeed = bytearray([parseSpeed(data)])
        speedMsg = can.Message(channel='can0',arbritation_id=0x503,data=sendSpeed,extended_id=False) ##Need to verify data parameter
        
        bus.send(speedMsg)
        message = bus.recv()	# Wait until a message is received.
		
        c = '{0:f} {1:x} {2:x} '.format(message.timestamp - prevTime, message.arbitration_id, message.dlc)
        s=''
        prevTime = message.timestamp
        for i in range(message.dlc):
            s +=  '{0:x} '.format(message.data[i])
		
        if int(hex(message.arbitration_id)[2:]) == temperatureID:
            leftFrontMotorTemperature = message.data[0] - 20
            leftRearMotorTemperature = message.data[1] - 20
            rightFrontMotorTemperature = message.data[2] - 20
            rightRearMotorTemperature = message.data[3] - 20
            batteryTemperature = message.data[4] - 20
        
        elif int(hex(message.arbritation_id[2:])) == vehicleID:
            maxPower = message.data[0] 
            soc = message.data[1]
            shutdown = message.data[2]
            speed = message.data[3]
            startupStatus = message.data[4]

        gm.setSpeed(speed)
        gm.setBatteryLevel(soc)
        gm.setBatteryTemperature(batteryTemperature)
        gm.setShutdown(shutdown)
        gm.setMotorTemperatureOne(leftFrontMotorTemperature)
        gm.setMotorTemperatureTwo(rightFrontMotorTemperature)
        gm.setMotorTemperatureThree(leftRearMotorTemperature)
        gm.setMotorTemperatureFour(rightRearMotorTemperature)
        gm.setStartupStatus(startupStatus)
        gm.setMaxPower(maxPower)
       

except KeyboardInterrupt:
	#Catch keyboard interrupt
	os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')	
