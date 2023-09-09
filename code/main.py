#!/usr/bin/env python3

import drivebase
import sensors
import comms
import brick
import behaviours

from menu import Menu, MenuButton

"""
	A \\__// C
	
   Left		Right

	B  Back  D

Front IR 	1
Compass 	2
Ultrasonic	3
Back IR 	4
			
"""

def close_menu(): raise KeyboardInterrupt

def main():
	"""Main loop"""

	kickoff_length = 20

	for _ in range(kickoff_length):
		sensors.UpdateValues()
		behaviours.Kickoff(drivebase,sensors.Values)

	while True:

		# Update button variables
		brick.buttons.process()

		# Stop program if middle or exit button pressed
		if brick.buttons.enter or brick.buttons.backspace: break

		# Update Sensors
		sensors.UpdateValues()

		# If we have the ball long enough, try score
		if sensors.Values.has_ball:
			behaviours.Score(drivebase,sensors.Values)
		
		# Otherwise if we can see the ball, chase it
		if sensors.Values.found_ball:
			behaviours.Chase(drivebase,sensors.Values)

		# If we cannot find the ball, wait	
		else:
			behaviours.ReturnToGoal(drivebase,sensors.Values)

	# Stop motors and reset brick color 
	drivebase.Coast()
	brick.Color('green')

# Define all our buttons and functions
menu_buttons = [
	MenuButton("Run Program",script=main),
	MenuButton("Calibrate Field",script=sensors.calibration.CalibrateField,args=[brick,drivebase,sensors]),
	MenuButton("Calibrate Ball",script=sensors.calibration.CalibrateBall,args=[brick,drivebase,sensors]),
	MenuButton("Exit",script=close_menu),
]

# Create Menu Class
menu = Menu([2,2], menu_buttons)

sensors.calibration.Load()

# If the program is started run the code
if __name__ == '__main__':
	brick.PlayTone(700)

	try:
		menu.Run()

	except KeyboardInterrupt:
		print("Keyboard Interrupt")
	
	except Exception as error:

		drivebase.ForceCoast()
		brick.Color('red')

		menu.Print(str(error),line_length=25)

		while not brick.buttons.backspace:
			brick.buttons.process()

	drivebase.Coast()
	brick.Color('green')