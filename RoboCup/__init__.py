#!/usr/bin/env python3

from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.sensor import Sensor
from ev3dev2.motor import SpeedPercent

from smbus import SMBus
from math import sin, cos, tan

# ev3dev API Reference:
# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/spec.html
# 
# RoboCup Module Example
# ExampleProject()


class Driver:
	IR = "ht-nxt-ir-seek-v2"
	COMPASS = "ht-nxt-compass"

def Unpack(values) -> list:
	for item in values:
		try:
			yield from Unpack(item)
		except TypeError:
			yield item

def Average(values) -> float:
	return sum(values) / len(values)

class Clamper():
	def __init__(self,min_value: int,max_value: int) -> None:
		self.min_value = min_value; self.max_value = max_value

	def Clamp(self,value: int) -> list:
		if value < self.min_value: value = self.min_value
		if value > self.max_value: value = self.max_value

		return value


	def ClampList(self,values: list) -> list:
		values = list(Unpack(values))
		clamped = [None] * len(values)

		for i,value in enumerate(values):
			if value < self.min_value: value = self.min_value
			if value > self.max_value: value = self.max_value

			clamped[i] = value

		return clamped

class PID_Controller():
	def __init__(self,p,i,d) -> None:
		self.kp = p; self.ki = i; self.kd = d;

		self.reset()

	def reset(self) -> None:
		self.last_error = 0

	def update(self,value: float) -> float:
		error = value - self.last_error

		p = self.kp * value
		i = value * error
		d = error

		return p + (self.ki * i) + (self.kd * d)

class DoubleInfrared():
	def __init__(self,sensor1,sensor2):
		self.sensors = [
			Sensor(sensor1[0], driver_name = Driver.IR),
			Sensor(sensor2[0], driver_name = Driver.IR),
		]

		self.angles = [sensor1[1], sensor2[1]]

		for s in self.sensors: s.mode = "AC-ALL"

	def true_value(self,sensor_id):
		return ( ( (self.sensors[sensor_id].value(0) - 5) * 30) + self.angles[sensor_id] ) / 30

	def proximity(self,sensor_id):
		return max([self.sensors[sensor_id].value(i) for i in range(1,5)])

	def read(self):
		front = self.true_value(0), self.proximity(0)
		back =  self.true_value(1), self.proximity(1)

		if front[1] > back[1]:
			return front

		return back 

	def close(self):
		pass

class IRSeeker360():
	def __init__(self,port:int):
		self.port = port if type(port) == int else int(port[-1])

		self.i2c_address = 0x08

		self.create_bus()

	def read(self):
		return self.bus.read_i2c_block_data(self.i2c_address, 0, 2)

		# # Read infrared sensor bin data from all 12 sensors
		raw_ir = [self.bus.read_i2c_block_data(self.i2c_address, i, 2) for i in range(12)]

		# # Fix invalid read data
		all_angles = [value for value in raw_ir[0] if 0 <= value <= 12]

		# # return Angle, Strength
		return max(set(all_angles), key = all_angles.count), max(set(raw_ir[1]), key = raw_ir[1].count)

	def create_bus(self):
		self.bus = SMBus(self.port + 0x2)

	def close(self):
		self.bus.close()

class FilteredSensor():
	def __init__(self,difference: int = 200, outliers: int = 15) -> None:
		self.stored = []
		self.counter = 0

		self.difference = difference
		self.outliers = outliers

	def Value(self,value) -> float:
		if self.counter > self.outliers: self.stored = []

		if len(self.stored) == 0: 
			self.stored.append(value)

		change = abs(self.Average(self.stored) - value)

		if change >= self.difference:
			self.counter += 1
		else:
			self.stored.append(value)

		return self.Average(self.stored)

class Robot():
	def __init__(self) -> None:
		self.Port = {
			"A": None,
			"B": None,
			"C": None,
			"D": None,
			"1": None,
			"2": None,
			"3": None,
			"4": None,
		}

		self.Leds = Leds()
		self.Sound = Sound()
		self.Buttons = Button()
		self.Display = Display()
		self.Speed = Clamper(-100,100)

	def CoastMotors(self) -> None:
		[self.Port[p].off(brake=False) for p in list("ABCD") if self.Port[p] != None]

	def ResetMotors(self) -> None:
		[self.Port[p].reset() for p in list("ABCD") if self.Port[p] != None]

	def Color(self,color) -> None:
		self.Leds.set_color('LEFT',color.upper())
		self.Leds.set_color('RIGHT',color.upper())

	def ScaleSpeeds(self,target_value:int,speeds:list) -> list:
		greatest = max([abs(speed) for speed in speeds])

		if greatest > target_value: greatest = target_value

		fix = target_value / greatest

		for i in range(len(speeds)):
			speeds[i] = round(speeds[i] * fix,2)

		return speeds

	def PrintPorts(self) -> None:
		print('\n'.join(["Port {}: {}".format(x,self.Port[x] != None) for x in self.Port]))

	def AngleToXY(self,angle,speed) -> tuple:
		x = speed * cos(angle)
		y = speed * sin(angle)

		return (x,y)

	def StartMotors(self,speeds) -> None:
		speeds = list(Unpack(speeds))
		for p in list("ABCD"):
			if self.Port[p] != None:
				self.Port[p].on(SpeedPercent(self.Speed.Clamp(speeds[0])))
				if len(speeds) > 1: speeds.pop(0)