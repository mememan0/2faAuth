#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import csv, subprocess, time
greenLed = 17 # Setup LED's
redLed = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(greenLed, GPIO.OUT)
GPIO.setup(redLed, GPIO.OUT)

global tic
global tok

def banner(): # Opening Banner

    print("""

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        Two Factor Autentication Using RFID And Bluetooth        
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

""")

def msg(type, text): # Debug Message formatting

    if type == int(1):
        print("[!] " + text)

    if type == int(2):
       print("[i] " + text)

def readCard(): # Reads UUID from card
    global tic
    msg(2,"Place Card On Reader...")
    try:
        reader = SimpleMFRC522()
        id, data = reader.read()
	tic = time.time()
	GPIO.output(redLed, GPIO.HIGH)
	time.sleep(0.2)
        msg(2,"Card ID:" + str(id))
	GPIO.output(redLed, GPIO.LOW)
        return str(id)
    except:
        msg(1,"Error in reading card")
        quit()



def quit(): # Cleanup
    msg(1, "Quitting...")
    GPIO.cleanup()

def checkFile(id): # Function to check if a UUID is valid

    with open('data.csv') as f:
        reader = csv.reader(f)
        data = list(reader)
        data = data[0]
    	storedId = []
        counter = 0
    	for i in range (0, int(len(data)/3)):
            storedId.append(data[counter])
            counter = counter + 3
	
        for approvedId in storedId:
	    if approvedId == id:
                msg(2, "Card Approved")
		return True
	    else:
		continue


def getStoredValue(id, itemNo): # Function to get a stored value from the data file
    with open('data.csv') as f:
        reader = csv.reader(f)
        data = list(reader)
        data = data[0]
        storedId = []
        counter = 0
        for i in range (0, int(len(data)/3)): # Load all UUID's
            storedId.append(data[counter])
            counter = counter + 3
        for approvedId in storedId: # Get position of UUID plus the item number we want to access
            if approvedId == id:
                listNumber = data.index(id)
		result = str(data[listNumber + itemNo])
                return str(result)
            else:
                continue

def connectBluetooth(id): # Function used to ping the bluetooth device
    msg(2, "User: " + getStoredValue(id, 2))
    msg(2, "Users Bluetooth MAC: " + getStoredValue(id, 1))
    btaddr = getStoredValue(id, 1)

    out = subprocess.Popen(['l2ping', '-c', '1', btaddr], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = out.communicate()
    output = stdout[0]


    if "44 bytes" in output: # Is there a reply of 44 bytes?
	msg(2, "Device Detected")
        msg(2, output[66:-29])
	return True
    else:
        msg(1, "Authentication Failed. Device Not Nearby")
	return False



def main(): # Main function
    banner()
    id = readCard()
    if checkFile(id) == True: # Is the RFID card valid?
	if connectBluetooth(id) == True: # Is the phone in range?
	    msg(2, "Authentication OK")
	    GPIO.output(greenLed, GPIO.HIGH)
            tok = time.time()
	    timer = tok - tic
	    msg(2, "Time Taken: " + str(timer) + " Seconds")
	    time.sleep(3)
	    GPIO.output(greenLed, GPIO.LOW)
	else:
	    GPIO.output(redLed, GPIO.HIGH)
	    time.sleep(3)
	    GPIO.output(redLed, GPIO.LOW)

    else:
        msg(1, "Invalid Card/ID")

main()
quit()
