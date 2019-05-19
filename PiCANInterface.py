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


print('\n\rCAN Rx test')
print('Bring up CAN0....')
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
dashboardID = 502

try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
	exit()
	
print('Ready')
prevTime = 0;

try:
	while True:
		message = bus.recv()	# Wait until a message is received.
		
		
		c = '{0:f} {1:x} {2:x} '.format(message.timestamp - prevTime, message.arbitration_id, message.dlc)
		s=''
		prevTime = message.timestamp
		for i in range(message.dlc ):
			s +=  '{0:x} '.format(message.data[i])
		
		if int(hex(message.arbitration_id)[2:]) == dashboardID:
                    # Do stuff with dash values
                    ## message.data[0-3] are motor temperatures (LF,LR,RF,RR), respectively
                    ## message.data[4] is vehicle speed
                    leftFrontMotorTemperature = message.data[0] - 20
                    leftRearMotorTemperature = message.data[1] - 20
                    rightFrontMotorTemperature = message.data[2] - 20
                    rightRearMotorTemperature = message.data[3] - 20
                    speed = message.data[4]
                    if message.data[5] >= 128:
                        soc = message.data[5] - 128
                    else:
                        soc = message.data[5]
                    if message.data[5] >= 128 and message.data[6] % 2 != 0:
                        startupStatus = 3
                    elif message.data[5] < 128 and message.data[6] % 2 != 0:
                        startupStatus = 2
                    elif message.data[5] >= 128 and message.data[6] % 2 == 0:
                        startupStatus = 1
                    else:
                        startupStatus = 0
                    maxPower = message.data[6] >> 1
                    vcuError = message.data[7]
                    batteryTemperature = 0
                    
                    print(leftFrontMotorTemperature)
                    
                    gm.setSpeed(speed)
                    gm.setBatteryLevel(soc)
                    gm.setBatteryTemperature(batteryTemperature)
                    gm.setShutdown(vcuError)
                    gm.setMotorTemperatureOne(leftFrontMotorTemperature)
                    gm.setMotorTemperatureTwo(rightFrontMotorTemperature)
                    gm.setMotorTemperatureThree(leftRearMotorTemperature)
                    gm.setMotorTemperatureFour(rightRearMotorTemperature)
                    gm.setHV(0)
                    gm.setLV(0)
                    gm.setMaxPower(maxPower)
                    
                    #print("Done")

except KeyboardInterrupt:
	#Catch keyboard interrupt
	os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')	
