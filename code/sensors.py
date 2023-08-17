from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *

from smbus import SMBus

global port

Compass = lambda port: Sensor(port,driver_name="ht-nxt-compass")
InfraredSensor = lambda port: Sensor(port,driver_name="ht-nxt-ir-seek-v2")

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

port = {
	"1": IRSeeker360(INPUT_1),
	"2": Compass(INPUT_2),
	"3": UltrasonicSensor(INPUT_3),
	"4": None
}

port["2"].mode = "COMPASS"