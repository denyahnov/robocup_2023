from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *

from custom_sensors import *

IR = IRSeeker360(INPUT_1)
Compass = Sensor(INPUT_2,driver_name="ht-nxt-compass")
Ultrasonic = UltrasonicSensor(INPUT_3)

Compass.mode = "COMPASS"

def ConvertAngle(angle):
	"""Convert 0 to 360 degrees -> -180 to 180 degrees"""

	return angle if angle <= 180 else angle - 360

def GetRelativeAngle(angle,relation):
	return ConvertAngle((((angle - relation) % 360) + 360) % 360)

def HasBall(strength):
	return strength > 50