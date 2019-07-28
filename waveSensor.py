#!/usr/bin/python -u
import sys
import getopt
from dronekit import connect
import time
import csv

address = 'localhost'
port = 9000

vehicle = connect('udpout:'+address+':'+str(port),wait_ready=False)

device = ''
instructions = "Usage:"

##Parse Command line options
############################
try:
    options, remainder = getopt.getopt(sys.argv[1:],"hd:f:",["help", "device=", "file="])
except:
    print(instructions)
    exit(1)

file = ''

for opt, arg in options:
    if opt in ('-h', '--help'):
        print(instructions)
        exit(1)
    elif opt in ('-d', '--device'):
        if (arg != ''):
            device = arg
    elif opt in ('-f', '--file'):
	if (arg != ''):
	    file = arg
    else:
        print(instructions)
        exit(1)

if (file is ''):
    file = "/home/pi/wave-logs/wave-"+time.strftime("%Y-%m-%d-%H-%M-%S")+".csv"

fout = open(str(file),'wb')
writer = csv.writer(fout,delimiter=',')

#Make a new Ping
print()
print("------------------------------------")
print("Starting Wave Log")
print("------------------------------------")

#Read and print distance measurements with confidence
writer.writerow(["Altitude | Lat | Lon"])
fout.close()

lastHeartbeat = vehicle.last_heartbeat
#lastMessageTime = vehicl

while True:
    #Limit to 10hz
    time.sleep(0.1)

    #Don't bother updating if we don't have a new mavlink packet
    if (vehicle.last_heartbeat > lastHeartbeat):
        lastHeartbeat = vehicle.last_heartbeat
        continue
    else:
        lastHeartbeat = vehicle.last_heartbeat

    print(" Alt: " + str(vehicle.location.global_frame.alt) +" | Lat: " + str(vehicle.location.global_frame.lat) + " | Lon: " + str(vehicle.location.global_frame.lon))
    fout = open(str(file),'a')
    writer = csv.writer(fout,delimiter=',')
    writer.writerow([str(vehicle.location.global_frame.alt),str(vehicle.location.global_frame.lat),str(vehicle.location.global_frame.lon)])
    fout.close()
