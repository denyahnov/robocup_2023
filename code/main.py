#!/usr/bin/env python3

import drivebase
import sensors
import calibration
import comms
import brick

from menu import *
from behaviours import *

from traceback import print_exc

def close_menu(self): raise KeyboardInterrupt

def main():
	"""Main loop"""

	# Change brick color to red
	brick.Color('red')

	DEBUG = []

	max_turn = 75
	
	kickoff_length = 60

	# Drive Straight for X amount of time
	for i in range(kickoff_length):
		Kickoff(drivebase)

	while True:

		# Update button variables
		brick.buttons.process()

		# Stop program if middle or exit button pressed
		if brick.buttons.enter or brick.buttons.backspace: break

		# Unpack IR data
		ball_angle, ball_strength = sensors.IR.read()

		# Compass Data
		compass = sensors.GetRelativeAngle(sensors.Compass.value(), calibration.goal_heading)

		ultrasonic = sensors.Ultrasonic.distance_centimeters - calibration.center_distance

		three_sixty_angle = sensors.ConvertAngle(ball_angle * 30)

		values = {
			"ball_angle": ball_angle,
			"ball_strength": ball_strength,
			"compass": compass,
			"ultrasonic": ultrasonic,
			"ball_360_angle": three_sixty_angle,
			"has_ball": sensors.HasBall(ball_strength),
		}

		Chase(drivebase,values)

		# Store data if we want to debug the robot
		if calibration.debug_mode:
			DEBUG.append([scaled_speeds,three_sixty_angle])

	# Stop motors and reset brick color 
	drivebase.Coast()
	brick.Color('green')

	# Save debug data
	if calibration.debug_mode:
		with open("{}.json".format(int(time())),"w") as file:
			dump(DEBUG,file)

# Define all our buttons and functions
menu_buttons = [
	MenuButton("Run Program",script=main),
	MenuButton("Calibrate",script=calibration.Calibrate,args=[drivebase,sensors]),
	MenuButton("Bluetooth: False",script=comms.Start),
	MenuButton("Exit",script=close_menu),
]

# Create Menu Class
menu = Menu([2,2], menu_buttons)

calibration.Load()

# If the program is started run the code
if __name__ == '__main__':
	brick.PlayTone(700)

	try:
		menu.Run()
	except KeyboardInterrupt:
		print("Keyboard Interrupt")
	except:
		print_exc()

	drivebase.Coast()
	brick.Color('green')

	sensors.IR.close()