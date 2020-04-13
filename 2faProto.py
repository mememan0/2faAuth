#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import csv

def banner():

    print("""

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        Two Factor Autentication Using RFID And Bluetooth        
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

""")

def msg(type, text):

    if type == int(1):
        print("[!] " + text)

    if type == int(2):
       print("[i] " + text)

def readCard():
    msg(2,"Place Card On Reader...")
    try:
        reader = SimpleMFRC522()
        id, data = reader.read()
        msg(2,"Card ID:" + str(id))
        return str(id)
    except:
        msg(1,"Error in reading card")
        quit()



def quit():
    msg(1, "Quitting...")
    GPIO.cleanup()

def checkFile(id):

    with open('data.csv') as f:
        reader = csv.reader(f)
        data = list(reader)
        data = data[0]
    	storedId = []
        counter = 0
    	for i in range (0, int(len(data)/2)):
            storedId.append(data[counter])
            counter = counter + 2
        for approvedId in storedId:
	    if approvedId == id:
                msg(2, "Card Approved")
		return True
	    else:
		continue
def getStoredValue(id, itemNo):
    with open('data.csv') as f:
        reader = csv.reader(f)
        data = list(reader)
        data = data[0]
        storedId = []
        counter = 0
        for i in range (0, int(len(data)/2)):
            storedId.append(data[counter])
            counter = counter + 2
        for approvedId in storedId:
            if approvedId == id:
                listNumber = data.index(id)
		result = str(data[listNumber + itemNo])
                return str(result)
            else:
                continue

def connectBluetooth(id):
    msg(2, "User: " + getStoredValue(id, 2))
    msg(2, "Users Bluetooth MAC: " + getStoredValue(id, 1))



def main():
    banner()
    id = readCard()
    if checkFile(id) == True:
	connectBluetooth(id)
    else:
        msg(1, "Invalid Card/ID")
    
main()
quit()
