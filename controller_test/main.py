#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
								 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import Ev3devSensor
import struct, time, math
from threading import Thread

global lx,ly,rx,ry
global goal_heading
global RUNNING

RUNNING = True

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

# Scaling function for converting stick values (0,255) to (-100,100)
def scale(val, src, dst):
	return (float(val-src[0]) / (src[1]-src[0])) * (dst[1]-dst[0])+dst[0]

def ToAngle(x,y) -> tuple:
	distance = math.sqrt(abs(pow(x,2) + pow(y,2)))
	angle = math.degrees(math.atan2(y, x)) - 90

	return distance, angle

def CalculateMotors(angle:float) -> list:
	"""Calculate 4 Motor speeds from an angle"""
	angle = math.radians(angle)

	# Math stuff
	front_left =  -1 * math.cos(math.pi / 4 - angle)
	front_right = 1 * math.cos(math.pi / 4 + angle)
	back_left =  -1 * math.cos(math.pi / 4 + angle)
	back_right = 1 * math.cos(math.pi / 4 - angle)

	# Returns the speeds in [A,B,C,D] form
	return [
		front_right, 	# Motor A
		front_left,		# Motor B
		back_right,		# Motor C
		back_left		# Motor D
	]

def Inverse(motors:list) -> list:
	"""Inverse certain motors"""
	return -motors[0],motors[1],motors[2],-motors[3]

def ScaleSpeeds(target_value:int,speeds:list) -> list:
	greatest = max([abs(speed) for speed in speeds])

	if greatest > target_value: greatest = target_value

	fix = target_value / greatest

	for i in range(len(speeds)):
		speeds[i] = round(speeds[i] * fix,2)

	return speeds

def Turn(motors:list,speed:float) -> list:
	"""Turn our robot at a certain speed"""
	return [motor + speed for motor in motors]

# Initialise brick and motors
ev3 = EV3Brick()
ev3.speaker.beep()

a = Motor(Port.A)
b = Motor(Port.B)
c = Motor(Port.C)
d = Motor(Port.D)

compass = Ev3devSensor(Port.S2)

goal_heading = compass.read("COMPASS")[0]

lx,ly,rx,ry = 0,0,0,0

def CalcThread():
	global RUNNING
	global lx,ly,rx,ry
	global goal_heading

	speed = Clamper(-100,100)

	while RUNNING:
		compass_ang = compass.read("COMPASS")[0] - goal_heading

		dist, angle = ToAngle(0 if -2 < lx < 2 else lx, 0 if -2 < ly < 2 else ly)

		dist = speed.Clamp(dist)

		speeds = CalculateMotors(angle - compass_ang)

		scaled = ScaleSpeeds(dist,speeds) if dist > 0 else [0,0,0,0]

		scaled = Turn(scaled,0 if -2 < rx < 2 else rx)

		a_speed,b_speed,c_speed,d_speed = Inverse(scaled)

		a.dc(speed.Clamp(a_speed))
		b.dc(speed.Clamp(b_speed))
		c.dc(speed.Clamp(c_speed))
		d.dc(speed.Clamp(d_speed))

thread = Thread(target=CalcThread)
thread.start()

# Setup for reading controller input
infile_path = "/dev/input/event4"
with open(infile_path, "rb") as in_file:
	FORMAT = 'llHHI'
	EVENT_SIZE = struct.calcsize(FORMAT)
	event = in_file.read(EVENT_SIZE)

	# Main loop
	while event:		
		# Read incoming event
		(tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

		# Joystick moved
		if ev_type == 3:

			if code == 0: # Left stick x
				lx = scale(value, (0,255), (-100,100))
				
			if code == 1: # Left stick y
				ly = scale(value, (0,255), (-100,100))

			if code == 3: # Right stick x
				rx = scale(value, (0,255), (-100,100))

			if code == 4: # Right stick y
				ry = scale(value, (0,255), (-100,100))

		# Button pressed
		if ev_type == 1:

			if code == 304: # X button
				pass

			if code == 305: # O button
				goal_heading = compass.read("COMPASS")[0]
			
			if code == 307: # △ button
				break

			if code == 308: # □ button
				pass

		# Read new event
		event = in_file.read(EVENT_SIZE)

RUNNING = False
ev3.speaker.beep()
