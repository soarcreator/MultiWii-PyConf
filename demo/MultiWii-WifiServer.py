import time
import threading
from MultiWiiWithSocket import MultiWiiSocketServer
import socket

# serialPort = "/dev/ttyUSB0"
serialPort = "/dev/tty.usbserial-AH01RI1Q"
server = MultiWiiSocketServer(serialPort, 6022)

try:
	while (1):
		data = server.connection.recv(2048)
		print(data)
		server.handleJsonData(data)
finally:
	server.connection.close()