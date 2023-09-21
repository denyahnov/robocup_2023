from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *

from custom_sensors import *

import calibration

from threading import Thread

frontIR = Sensor(INPUT_1,driver_name="ht-nxt-ir-seek-v2")
backIR = Sensor(INPUT_4,driver_name="ht-nxt-ir-seek-v2")
Compass = Sensor(INPUT_2,driver_name="ht-nxt-compass")
Ultrasonic = UltrasonicSensor(INPUT_3)

frontIR.mode = "AC-ALL"
backIR.mode = "AC-ALL"

Compass.mode = "COMPASS"

Ultrasonic.mode = "US-DIST-CM"

# Calibration Values
HOLD_ANGLE = 20

HOLD,NEAR = 0,1 # Used for getting ball calibration data

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
# robot_running:	True or False

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

	robot_running = False

def main_loop():
	while True:
		UpdateValues()

def UpdateForever():
	thread = Thread(target=main_loop)
	thread.daemon = True

	thread.start()

def UpdateValues():

	raw_front, raw_back = frontIR.value(), backIR.value()

	front = (raw_front - 5) % 12, max([frontIR.value(i + 1) for i in range(5)])
	back = (raw_back + 1) % 12, max([backIR.value(i + 1) for i in range(5)])

	if front[1] > back[1]:
		Values.ball_direction, Values.ball_strength = front
	else:
		Values.ball_direction, Values.ball_strength = back

	Values.ball_angle = ConvertAngle(Values.ball_direction * 30)

	Values.compass = GetRelativeAngle(Compass.value(), calibration.goal_heading)

	Values.ultrasonic = Ultrasonic.distance_centimeters - calibration.center_distance

	Values.touch_sensor = False

	Values.near_ball = NearBall()
	
	Values.has_ball = HasBall()

	Values.found_ball = (raw_front + raw_back) != 0 and FoundBall()

def ConvertAngle(angle):
	"""Convert 0 to 360 degrees -> -180 to 180 degrees"""

	return angle if angle <= 180 else angle - 360

def GetRelativeAngle(angle,relation):
	return ConvertAngle((((angle - relation) % 360) + 360) % 360)

def FoundBall():
	return Values.ball_strength > 3

def HasBall():
	return (Values.ball_strength >= calibration.ball_strengths[Values.ball_direction][HOLD]) and (-HOLD_ANGLE <= Values.ball_angle <= HOLD_ANGLE)

def NearBall():
	return Values.ball_strength >= calibration.ball_strengths[Values.ball_direction][NEAR]