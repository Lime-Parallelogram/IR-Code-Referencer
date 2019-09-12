import RPi.GPIO as GPIO
from datetime import datetime

pin = 11
Buttons = [0x300ff9867L, 0x300ffd827L, 0x300ff8877L, 0x300ffa857L, 0x300ffe817L, 0x300ff48b7L, 0x300ff6897L, 0x300ff02fdL, 0x300ff32cdL, 0x300ff20dfL]
ButtonsNames = ["RED",   "GREEN",      "BLUE",       "WHITE",      "DARK ORANGE","LIGHT GREEN","DARK BLUE",  "VIBRANT ORANGE","LIGHT BLUE","DARK PURPLE"]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)

def getBinary():
	num1s = 0
	binary = 1
	command = []
	previousValue = 0
	value = GPIO.input(pin)
	
	while value:
		value = GPIO.input(pin)
		
	startTime = datetime.now()
	
	while True:
		if previousValue != value:
			now = datetime.now()
			pulseTime = now - startTime
			startTime = now
			command.append((previousValue, pulseTime.microseconds))
			
		if value:
			num1s += 1
		else:
			num1s = 0
		
		if num1s > 10000:
			break
			
		previousValue = value
		value = GPIO.input(pin)
		
	for (typ, tme) in command:
		if typ == 1:
			if tme > 1000:
				binary = binary *10 +1
			else:
				binary *= 10
			
	if len(str(binary)) > 34:
		binary = int(str(binary)[:34])
		
	return binary
	
def convertHex(binaryValue):
	tmpB2 = int(str(binaryValue),2)
	return hex(tmpB2)
	
while True:
	inData = convertHex(getBinary())
	for button in range(len(Buttons)):
		if hex(Buttons[button]) == inData:
			print(ButtonsNames[button])
			
