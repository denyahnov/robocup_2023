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

	speeds = Clamp(speeds)

	motors["A"].run_forever(speed_sp=SpeedPercent(-speeds[0]))
	motors["B"].run_forever(speed_sp=SpeedPercent(speeds[1]))
	motors["C"].run_forever(speed_sp=SpeedPercent(speeds[2]))
	motors["D"].run_forever(speed_sp=SpeedPercent(-speeds[3]))

def Reset():
	global motors

	[motors[i].reset() for i in motors]

def Coast():
	global motors

	[motors[i].off(brake=False) for i in motors]

def Turn(speeds,turn_speed):
	return [s + turn_speed for s in speeds]

def TurnToHeading(angle):
	return angle * 1.8

def IsStalled():
	return any([motors[i].is_stalled for i in motors])

def Clamp(speeds):
	return [min(100, max(-100,i)) for i in speeds]