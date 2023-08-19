from ev3dev2.motor import *

import math

global motors

motors = {port: MediumMotor("out" + port) for port in "ABCD"}

DRIVEBASE_SPEED = 90

# A and D are negative

def MoveTo(angle:float) -> list:
	"""Calculate 4 Motor speeds from an angle"""
	angle = math.radians(angle)

	# Math stuff
	front_left =  -math.cos(math.pi / 4 - angle)
	front_right = math.cos(math.pi / 4 + angle)
	back_left = -math.cos(math.pi / 4 + angle)
	back_right = math.cos(math.pi / 4 - angle)

	# Returns the speeds in [A,B,C,D] form
	return [
		front_left, 	# Motor A
		back_left,		# Motor B
		front_right,	# Motor C
		back_right,		# Motor D
	]

def ScaleSpeeds(speeds:list,target_value:int = DRIVEBASE_SPEED) -> list:
	greatest = max([abs(speed) for speed in speeds])

	return [round(s * (target_value / greatest)) for s in speeds]

def Drive(speeds):
	global motors

	motors["A"].on(SpeedPercent(-speeds[0]))
	motors["B"].on(SpeedPercent(speeds[1]))
	motors["C"].on(SpeedPercent(speeds[2]))
	motors["D"].on(SpeedPercent(-speeds[3]))

def Reset():
	global motors

	[motors[i].reset() for i in motors]

def Coast():
	global motors

	[motors[i].off(brake=False) for i in motors]

def Turn(turn_speed,speeds):
	return [s + turn_speed for s in speeds]

def TurnToHeading(angle):
	return angle * 2

def IsStalled():
	return any([motors[i].is_stalled for i in motors])