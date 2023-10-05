from ev3dev2.motor import *

import math

global motors

motors = {port: MediumMotor("out" + port) for port in "ABCD"}

DRIVEBASE_SPEED = 15

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

	speeds = ScaleSpeeds(speeds)

	speeds = Clamp(speeds)

	motors["A"].run_forever(speed_sp=-speeds[0] * motors["A"].max_speed / 100)
	motors["B"].run_forever(speed_sp=speeds[1] * motors["B"].max_speed / 100)
	motors["C"].run_forever(speed_sp=speeds[2] * motors["C"].max_speed / 100)
	motors["D"].run_forever(speed_sp=-speeds[3] * motors["D"].max_speed / 100)

def DriveSeconds(seconds,speeds):
	global motors

	speeds = ScaleSpeeds(speeds)
	
	speeds = Clamp(speeds)

	motors["A"].on_for_seconds(SpeedPercent(-speeds[0]),seconds,block=False)
	motors["B"].on_for_seconds(SpeedPercent(speeds[1]),seconds,block=False)
	motors["C"].on_for_seconds(SpeedPercent(speeds[2]),seconds,block=False)
	motors["D"].on_for_seconds(SpeedPercent(-speeds[3]),seconds,block=True)

def Reset():
	global motors

	[motors[i].reset() for i in motors]

def Coast():
	global motors

	[motors[i].off(brake=False) for i in motors]

def ForceCoast():
	global motors

	for port in motors:
		try:
			motors[port].off(brake=False)
		except:
			pass

def Turn(speeds,turn_speed):
	return [s + turn_speed for s in speeds]

def TurnToHeading(angle):
	return (angle + 2) * 1.5

def IsStalled():
	return any([motors[i].is_stalled for i in motors])

def Clamp(speeds):
	return [min(100, max(-100,i)) for i in speeds]