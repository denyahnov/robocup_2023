from smbus import SMBus

class IRSeeker360():
	def __init__(self,port:int):
		self.port = port if type(port) == int else int(port[-1])

		self.i2c_address = 0x08

		self.create_bus()

	def read(self):
		return self.bus.read_i2c_block_data(self.i2c_address, 0, 2)

	def create_bus(self):
		self.bus = SMBus(self.port + 0x2)

	def close(self):
		self.bus.close()