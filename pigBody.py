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
		self.heads = [] #lefts
		self.tails = [] #rights

		self.insertMode = False
		self.lrforward = True
		self.rlforward = True

		self.ready_inputs = []
		self.outputs = []

		try:
			temp = pigSocket.pigListener('right','localhost',36757)
			self.ready_inputs.append(temp)
		except socket.error as e:
			print(e)

		if(platform.system() == 'Linux'):
			self.ready_inputs.append(sys.stdin)
			sys.stdout.write('>')
			sys.stdout.flush()
		else:
			print("Non-linux system detected. stdin will not be available.")
			#print("Please use command line parameters or a config file.")

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
				
				if isinstance(fds,pigSocket.pigListener) and not fds.accepted:
					fds = fds.pigAccept(True)
					self.ready_inputs.append(fds)
					self.headsOrTails(fds)

				if fds == sys.stdin or isinstance(fds,pigSocket.adminSocket):
					if(fds == sys.stdin):
						keyboard = sys.stdin.readline()
					else:
						keyboard = fds.recv(1024)

					if(keyboard.strip() == 'i'):
						self.insertMode = True
						print("inserting:")
						break

					if(self.insertMode):
						if(keyboard.strip() == 'q'):
							self.insertMode = False
							break
						else:
							for srocket in self.tails + self.heads:
								srocket.send(keyboard.encode("utf-8"))	
						break

					inputcommands = pigCommands.commandInput(self,keyboard)
					for command in inputcommands:
						try:
							if(command.sType == 'client'):
								nSocket = pigSocket.pigConnector(command.side,command.address,command.port)
							elif(command.sType == 'server'):
								nSocket = pigSocket.pigListener(command.side,command.address,int(command.port))
								self.ready_inputs.append(nSocket)
							self.headsOrTails(nSocket)

						except socket.error as e:
							print(e)
					
					sys.stdout.write('>')
					sys.stdout.flush()				

				else:
					print(fds)
					data = fds.recv(1024)
					if data:
						try:
							print(data.decode("utf-8"))
						except:
							print("utf-8 incompatible data received")

						if(fds.side == 'left'):
							for srocket in self.tails: #left/head sends to right/tails
								srocket.send(data)
						if(fds.side == 'right'):
							for srocket in self.heads: #right/tails send to left/heads
								srocket.send(data)
					else:
						fds.close()
						self.ready_inputs.remove(fds)
						print("Client has disconnected")


pig = PigBody()
