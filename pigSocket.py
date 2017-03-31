import socket

#Avery VanKirk, March 2017
#socket handeling for python piggy

#Wrapper for socket
class pigSocket:
	def __init__(self,side,socket,accepted = False):
		self.side = side
		self.socket = socket
		self.accepted = accepted

	#Socket wrapper functions
	def fileno(self):
		return self.socket.fileno()

	#Here is where we will configure if socket wants to send or not.
	def send(self,data):
		return self.socket.send(data)

	def recv(self,size):
		return self.socket.recv(size)

	def close(self):
		return self.socket.close()

#subclass for a passive/listening/server socket
class pigListener(pigSocket):
	def __init__(self,side,address,port):
		self.side = side
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((address,port))
		self.socket.listen(5)
		super().__init__(side,self.socket)

	#passing in True for keepOpen spanws a new socket for the connction
	#and allows you to keep listening with the original
	def pigAccept(self,keepOpen = False):
		if(keepOpen):
			nSocket,nAddress = self.socket.accept()
			new = pigSocket(self.side,nSocket)
			return new
		else:
			self.socket,self.address = self.socket.accept()
			self.accepted = True
			return self

#for active/connecting socket
class pigConnector(pigSocket):
	def __init__(self,side,address,port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((address, int(port)))
		super().__init__(side,self.socket)

#listening socket for interacting with pig without stdin
class adminSocket(pigListener):
	def __init__(self):
		self.password = 'password'
		super().__init__(None,'localhost',39000)

	def pigAccept(self,password):
		if(self.password == password):
			self.socket,self.address = self.socket.accept()
			self.accepted = True
			return self