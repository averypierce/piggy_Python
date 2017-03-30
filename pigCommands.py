#command parser function for pythonPig


class connectionParams(object):
	def __init__ (self,side,address,port):
		self.side = side		
		self.address = address
		self.port = port

# Builds list of connectionParams and returns them for processing
def commandInput(self,line):
	input = line.split()

	clients = []
	servers = []

	for i in range(0,len(input)):
		#sample: -connect right localhost 36751
		if(input[i] == '-connect'):
			side = input[i+1]
			address = input[i+2]
			port = input[i+3]
			clients.append(connectionParams(side,address,port))
			i = i + 3

		#sample: -listen left 36751
		if(input[i] == '-listen'):
			side = input[i+1]
			address = 'localhost'
			port = input[i+2]
			servers.append(connectionParams(side,address,port))
			i = i + 2

	return clients,servers





