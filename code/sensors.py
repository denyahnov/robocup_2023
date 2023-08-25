from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *

from custom_sensors import *

IR = IRSeeker360(INPUT_1)
Compass = Sensor(INPUT_2,driver_name="ht-nxt-compass")
Ultrasonic = UltrasonicSensor(INPUT_3)

Compass.mode = "COMPASS"

# VALUE DICTIONARY:
# =============================
# ball_angle: 		-180 to 180
# ball_direction: 	0 to 12
# ball_strength: 	0 to ~150
# compass: 			-180 to 180
# ultrasonic: 		-130 to ~130
# touch_sensor:		True or False
# has_ball:			True or False
# near_ball:		True or False
# found_ball:		True or False

class Values:
	ball_angle = 0
	ball_direction = 0
	ball_strength = 0
	compass = 0
	ultrasonic = 0
	touch_sensor = False
	has_ball = False
	near_ball = False
	found_ball = False

def UpdateValues(calibration):
	Values.ball_direction, Values.ball_strength = IR.read()

	Values.ball_angle = ConvertAngle(Values.ball_direction * 30)

	Values.compass = GetRelativeAngle(Compass.value(), calibration.goal_heading)

	Values.ultrasonic = Ultrasonic.distance_centimeters - calibration.center_distance

	Values.touch_sensor = False

	Values.near_ball = NearBall()
	
	Values.has_ball = HasBall()

	Values.found_ball = FoundBall()

def ConvertAngle(angle):
	"""Convert 0 to 360 degrees -> -180 to 180 degrees"""

	return angle if angle <= 180 else angle - 360

def GetRelativeAngle(angle,relation):
	return ConvertAngle((((angle - relation) % 360) + 360) % 360)

def FoundBall():
	return Values.ball_strength > 0

def HasBall():
	return (Values.ball_strength >= 60) and (-20 <= Values.ball_angle <= 20)

def NearBall():
	return Values.ball_strength >= 40