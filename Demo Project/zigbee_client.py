#! /usr/bin/python

import serial
import time
import socket # for socket
import sys
from xbee import ZigBee


serial_port = serial.Serial('/dev/cu.usbserial-00000000', 9600)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Socket successfully created"
except socket.error as err:
    print "socket creation failed with error %s" %(err)

# default port for socket
port = 8899

try:
    host_ip = socket.gethostbyname('dc02.utdallas.edu')
except socket.gaierror:

    # this means could not resolve the host
    print "there was an error resolving the host"
    sys.exit()

# connecting to the server
s.connect((host_ip, port))

print "the socket has successfully connected to dc machine on port == %s" %(host_ip)
#print s.recv(1024)

def print_data(data):
    """
    This method is called whenever data is received
    from the associated XBee device. Its first and
    only argument is the data contained within the
    frame.
    """

    myData = data['rf_data']
    print "Zigbee Frame ", data
    print "Extracted Data ", myData
    fd = open("log.txt", "a")
    fd.write(myData.decode("utf-8") + "\n")
    fd.close()
    s.send(myData)
    print "Extracted data sent to server", "\n"

xbee = ZigBee(serial_port, callback=print_data)

while True:
    try:
        time.sleep(0.001)
    except KeyboardInterrupt:
        break

xbee.halt()
serial_port.close()