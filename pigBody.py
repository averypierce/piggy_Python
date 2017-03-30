#Piggy, Python edition
#Avery VanKirk, March 2017

#This is the core of the program that the rest is centered around.

import select
import socket
import sys
import pigSocket
import pigCommands
import platform
import atexit

def quit():
	print('Piggy Closed')

atexit.register(quit)

class PigBody():

	def __init__(self):
		self.heads = []
		self.tails = []

		self.lrforward = True
		self.rlforward = True

		self.ready_inputs = []
		self.outputs = []

		if(platform.system() == 'Linux'):
			self.ready_inputs.append(sys.stdin)
			sys.stdout.write('>')
			sys.stdout.flush()
		else:
			print("Non-linux system detected. stdin will not be available.")
			#print("Please use command line parameters or a config file.")

		#self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.clientsocket.connect(('192.168.2.16', 8888))
		#self.outputs.append(self.clientsocket)
		#self.append(self.clientsocket)

		#
		try:
			temp = pigSocket.pigSocket().buildSocket('right','localhost',36757)
			self.ready_inputs.append(temp)
		except:
			pass


		self.main()

	#Assigns a pigSocket to its appropriate list for message sending
	def headsOrTails(self,pigSocket):
		if(pigSocket.side == 'left' or pigSocket.side == 'l'):
			self.heads.append(pigSocket)
		elif(pigSocket.side == 'right' or pigSocket.side == 'r'):
			self.tails.append(pigSocket)

	def main(self):
		while True:
			readable, writable, error = select.select(self.ready_inputs,[], [])

			for fds in readable:
				
				if fds == sys.stdin:
					keyboard = sys.stdin.readline()
					clients,servers = pigCommands.commandInput(self,keyboard)
					for client in clients:
						try:
							cSocket = pigSocket.pigSocket().pigConnect(client.side,client.address,client.port)
							self.headsOrTails(cSocket)
						except socket.error as e:
							print(e)
					for server in servers:
						try:
							sSocket = pigSocket.pigSocket().buildSocket(server.side,server.address,int(server.port))
							self.ready_inputs.append(sSocket)
							self.headsOrTails(sSocket)
						except socket.error as e:
							print("Error: port " + server.port + " already in use.")
					sys.stdout.write('>')
					sys.stdout.flush()

				if isinstance(fds,pigSocket.pigSocket) and not fds.accepted:
					#cSocket,cAddr = fds.pigAccept()
					#temp = pigSocket.acceptedPigSocket(fds.side,cSocket)
					fds = fds.pigAccept(True)
					self.ready_inputs.append(fds)
					self.headsOrTails(fds)

				else:
					data = fds.recv(1024)
					if data:
						try:
							print(data.decode("utf-8") )
						except:
							print("utf-8 incompatible data received")
						#print(fds.side)
						#Still needs replaced with headsortails()
						if(fds.side == 'left'):
							for srocket in self.tails:
								srocket.send(data)
						if(fds.side == 'right'):
							for srocket in self.heads:
								print("well?!")
								srocket.send(data)
					else:
						fds.close()
						self.ready_inputs.remove(fds)
						print("Client has disconnected")


pig = PigBody()

#x = pigSocket.pigSocket('localhost',36751)
#ready_inputs.append(x)
#ready_inputs.append(pigSocket.pigSocket('localhost',36752))
