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

try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
##	GPIO.output(led,False)
	exit()

# Main loop
prevTime = 0;
question = 0;
try:
	while True:
		#GPIO.output(led,True)
                
		msg = can.Message(arbitration_id=0x50,data= [question],extended_id=False)
		bus.send(msg)
		count = count + 1
		if question == 255:
                    question = 0
		else:
                    question = question + 1
                    
		time.sleep(0.01)	
		print(count)
		print(question)
		
		message = bus.recv()	# Wait until a message is received.
		
		c = '{0:f} {1:x} {2:x} '.format(message.timestamp - prevTime, message.arbitration_id, message.dlc)
		s=''
		prevTime = message.timestamp
		for i in range(message.dlc ):
			s +=  '{0:x} '.format(message.data[i])
			
		print(' {}'.format(c+s))
		 

	
except KeyboardInterrupt:
	#Catch keyboard interrupt
	#GPIO.output(led,False)
	os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')	
