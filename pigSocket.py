import socket

#Avery VanKirk, March 2017
#socket handeling for python piggy


class pigSocket:
	def __init__(self):
		self.accepted = False
		self.side = None
		self.socket = None
		self.address = None

	#builds a new pasive/listening socket
	def buildSocket(self,side,address,port):
		self.side = side
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((address,port))
		self.socket.listen(5)
		return self

	#use this if you have a premade socket you want to wrap
	def takeSocket(self,side,socket):
		self.accepted = True
		self.side = side
		self.socket = socket

	#passing in True for keepOpen spanws a new socket for the connction
	#and allows you to keep listening with the original
	def pigAccept(self,keepOpen = False):
		if(keepOpen):
			new = pigSocket()
			nSocket,nAddress = self.socket.accept()
			new.takeSocket(self.side,nSocket)
			return new
		else:
			self.socket,self.address = self.socket.accept()
			self.accepted = True
			return self

	#builds a new active/connecting socket
	def pigConnect(self,side,address,port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((address, int(port)))
		return self

	#Socket wrapper functions
	def fileno(self):
		return self.socket.fileno()

	def send(self,data):
		return self.socket.send(data)

	def recv(self,size):
		return self.socket.recv(size)

	def close(self):
		return self.socket.close()