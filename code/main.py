#!/usr/bin/env python3

import drivebase
import sensors
import calibration
import comms
import brick

from menu import Menu, MenuButton

def close_menu(self): raise KeyboardInterrupt

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

def main():
	"""Main loop"""

	# Change brick color to red
	brick.Color('red')

	DEBUG = []

	speed = 90
	max_turn = 75
	
	ball_prox = 50

	while True:

		# Update button variables
		brick.buttons.process()

		# Stop program if middle or exit button pressed
		if brick.buttons.enter or brick.buttons.backspace: break

		# Unpack IR data
		ball_angle, ball_strength = sensors.port['1'].read()

		# Compass Data
		compass = drivebase.GetRelativeAngle(sensor.port['2'].value(), calibration.goal_heading)

		three_sixty_angle = drivebase.ConvertAngle(ball_angle * 30)

		if ball_strength > ball_prox: three_sixty_angle *= 1.5

		# Calculate the 4 motor speeds
		# Scale the speeds to our target speed
		scaled_speeds = drivebase.ScaleSpeeds(speed, drivebase.MoveTo(three_sixty_angle))

		# Clamp turn value to the `max_turn` variable
		turned_speeds = drivebase.Turn(speeds, drivebase.Compensate(compass))

		# Run the motors at desired speeds
		drivebase.Drive(drivebase.ScaleSpeeds(speed,turned_speeds))

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


# If the program is started run the code
if __name__ == '__main__':
	brick.PlayTone(700)

	menu.Run()

	drivebase.Coast()
	brick.Color('green')

	sensors.port['1'].close()