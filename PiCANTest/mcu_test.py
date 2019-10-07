#!/usr/bin/python3
#
# simple_tx_test.py
# 
# This python3 sent CAN messages out, with byte 7 increamenting each time.
# For use with PiCAN boards on the Raspberry Pi
# http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-2-p-1475.html
#
# Make sure Python-CAN is installed first http://skpang.co.uk/blog/archives/1220
#
# 01-02-16 SK Pang
#
#
#


import RPi.GPIO as GPIO
import can
import time
import os


#led = 22
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(led,GPIO.OUT)
#GPIO.output(led,True)

count = 0

print('\n\rCAN Rx test')
print('Bring up CAN0....')

# Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)	
print('Press CTL-C to exit')

prevTimeAV1 = 0
prevTimeAV2 = 0

systemReady = 0
error = 0
warn = 0
quitDcOn = 0
dcOn = 0
quitInverterOn = 0
inverterOn = 0
derating = 0
torqueCurrent = 0
magnetizingCurrent = 0

errorInfo = 0
tempIGBT = 0
tempInverter = 0
tempMotor = 0

inverterState = 0

try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
##	GPIO.output(led,False)
	exit()

# Main loop
try:
	while True:
		
		message = bus.recv()	# Wait until a message is received.
		if message.arbitration_id == 0x284:
			c = '{0:f} {1:x} {2:x} '.format(message.timestamp - prevTimeAV1, message.arbitration_id, message.dlc)
			prevTimeAV1 = message.timestamp
			systemReady = message.data[1] & 0x01
			error = message.data[1] & 0x02
			warn = message.data[1] & 0x08
			quitDcOn = message.data[1] & 0x04
			dcOn = message.data[1] & 0x10
			quitInverterOn = message.data[1] & 0x20
			inverterOn = message.data[1] & 0x40
			derating = message.data[1] & 0x80
			
		elif message.arbitration_id == 0x286:
			c = '{0:f} {1:x} {2:x} '.format(message.timestamp - prevTimeAV2, message.arbitration_id, message.dlc)
			prevTimeAV2 = message.timestamp
		
		
		if(inverterState == 0):
			if(systemReady == 1):
				inverterState = 1
		elif(inverterState == 1):
			if(systemReady == 1):
		elif(inverterState == 2):
			
		elif(inverterState == 3):
			
		elif(inverterState == 4):
		
		
		msg = can.Message(arbitration_id=0x501,data= [0x05,0x06, count & 0xff],extended_id=False)
		bus.send(msg)
		time.sleep(0.05)	
		print(count)	
		 

	
except KeyboardInterrupt:
	#Catch keyboard interrupt
	#GPIO.output(led,False)
	os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')	
