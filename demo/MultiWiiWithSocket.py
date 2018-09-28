from pymultiwii import MultiWii
import socket
import time
import threading
import json

class MultiWiiSocketServer(MultiWii):
	def __init__(self, serPort, port):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind(("0.0.0.0", port))
		self.server.listen(1)

		print("Waiting for client...")
		self.connection, self.clientAddress = self.server.accept()
		print(self.connection)
		print(self.clientAddress)

		MultiWii.__init__(self, serPort)

		# start Update on different thread

	def handleData(self, needToReturn, code, dataLenght, data):
		if needToReturn == False:
			self.sendCMD(dataLenght, code, data)
			self.connection.send(";")
			return None

		d = self.getData(code)
		if d == None:
			d = { "data": "" }
		self.connection.send(json.dumps(d))

		return d

	def handleCSVData(self, csv):
		data = csv.split(',')
		return self.handleData(data[0] == 1, int(data[1]), int(data[2]), [])

	def handleJsonData(self, jsonString):
		data = json.loads(jsonString)
		return self.handleData(data["return"] == 1, data["code"], data["dataLength"], data["data"])


class MultiWiiWithSocket:
	def __init__(self, ip, port):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((ip, port))

	def sendCMD(self, dataLength, code, data):
		self.client.send(json.dumps({"return": 0, "code": code, "dataLength": dataLength, "data": data}))
		self.client.recv(1)

	def getData(self, code):
		self.client.send(json.dumps({"return": 1, "code": code, "dataLength": 0, "data": []}))
		return json.loads(self.client.recv(2048))

	def arm(self):
		start = time.time()
		while time.time() - start < 0.5:
			data = [1500,1500,2000,1000]
			self.sendCMD(8, MultiWii.SET_RAW_RC, data)
			time.sleep(0.05)

	def disarm(self):
		start = time.time()
		while time.time() - start < 0.5:
			data = [1500,1500,1000,1000]
			self.sendCMD(8, MultiWii.SET_RAW_RC, data)
			time.sleep(0.05)