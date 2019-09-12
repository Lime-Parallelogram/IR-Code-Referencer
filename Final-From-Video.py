#-----------------------------------------#
#Name - IR-Finalised.py
#Description - The finalised code to read data from an IR sensor and then refernce it with stored values
#Author - Lime Parallelogram
#Licence - Compleatly Free
#Date - 12/09/2019
#------------------------------------------------------------#
#Imports modules
import RPi.GPIO as GPIO
from datetime import datetime

#Static program vars
pin = 11 #Input pin of sensor (GPIO.BOARD)
Buttons = [0x300ff9867L, 0x300ffd827L, 0x300ff8877L, 0x300ffa857L, 0x300ffe817L, 0x300ff48b7L, 0x300ff6897L, 0x300ff02fdL, 0x300ff32cdL, 0x300ff20dfL] #HEX code list
ButtonsNames = ["RED",   "GREEN",      "BLUE",       "WHITE",      "DARK ORANGE","LIGHT GREEN","DARK BLUE",  "VIBRANT ORANGE","LIGHT BLUE","DARK PURPLE"] #String list in same order as HEX list

#Sets up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)

#Gets binary value
def getBinary():
	#Internal vars
	num1s = 0 #Number of consecutive 1s read
	binary = 1 #The bianry value
	command = [] #The list to store pulse times in
	previousValue = 0 #The last value
	value = GPIO.input(pin) #The current value
	
	#Waits for the sensor to pull pin low
	while value:
		value = GPIO.input(pin)
		
	#Records start time
	startTime = datetime.now()
	
	while True:
		#If change detected in value
		if previousValue != value:
			now = datetime.now()
			pulseTime = now - startTime #Calculate the time of pulse
			startTime = now #Reset start time
			command.append((previousValue, pulseTime.microseconds)) #Store recorded data
			
		#Updates consecutive 1s variable
		if value:
			num1s += 1
		else:
			num1s = 0
		
		#Breaks program when the amount of 1s surpasses 10000
		if num1s > 10000:
			break
			
		#Re-reads pin
		previousValue = value
		value = GPIO.input(pin)
		
	#Converts times to binary
	for (typ, tme) in command:
		if typ == 1: #If looking at rest period
			if tme > 1000: #If pulse greater than 1000us
				binary = binary *10 +1 #Must be 1
			else:
				binary *= 10 #Must be 0
			
	if len(str(binary)) > 34: #Sometimes, there is some stray characters
		binary = int(str(binary)[:34])
		
	return binary
	
#Conver value to hex
def convertHex(binaryValue):
	tmpB2 = int(str(binaryValue),2) #Tempary propper base 2
	return hex(tmpB2)
	
while True:
	inData = convertHex(getBinary()) #Runs subs to get incomming hex value
	for button in range(len(Buttons)):#Runs through every value in list
		if hex(Buttons[button]) == inData: #Checks this against incomming
			print(ButtonsNames[button]) #Prints corresponding english name for button
			
