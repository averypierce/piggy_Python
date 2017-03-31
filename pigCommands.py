#command parser function for pythonPig


class connectionParams(object):
	def __init__ (self,side,address,port,sType):
		self.side = side		
		self.address = address
		self.port = port
		self.sType = sType

# Builds list of connectionParams and returns them for processing
def commandInput(self,line):
	input = line.split()

	commands = []

	for i in range(0,len(input)):
		#sample: -connect right localhost 36751
		if(input[i] == '-connect' or input[i] == '-listen'):
			side = input[i+1]
			address = input[i+2]
			port = input[i+3]
			commands.append(connectionParams(side,address,port,'client'))
			i = i + 3

		#sample: -listen left 36751
		#if(input[i] == '-listen'):
			#side = input[i+1]
			#address = 'localhost'
			#port = input[i+2]
			#commands.append(connectionParams(side,address,port,'server'))
			#i = i + 2

	return commands





