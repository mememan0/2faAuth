#!/usr/bin/env python3

print("Prorgam to add user to the data file")

username = str(input("User: "))
cardUUID = str(input("CardUUID: "))
btaddr = str(input("BtAddr: "))

with open("data.csv", "a+") as f:
    f.write(username + "," + cardUUID + "," + btaddr + ",")

