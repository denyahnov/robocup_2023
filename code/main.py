#!/usr/bin/env python3

import drivebase
import sensors
import calibration
import comms
import brick
import behaviours

from menu import Menu, MenuButton

from traceback import print_exc

def close_menu(self): raise KeyboardInterrupt

def main():
	"""Main loop"""

	while True:

		# Update button variables
		brick.buttons.process()

		# Stop program if middle or exit button pressed
		if brick.buttons.enter or brick.buttons.backspace: break

		# Update Sensors
		sensors.UpdateValues(calibration)

		# If we have the ball long enough, try score
		if sensors.Values.has_ball:
			# brick.Color('red')
			brick.PlayTone(500)
			behaviours.Score(drivebase,sensors.Values)
		
		# Otherwise if we can see the ball, chase it
		elif sensors.Values.found_ball:
			# brick.Color('orange')
			behaviours.Chase(drivebase,sensors.Values)

		# If we cannot find the ball, wait
		else:
			# brick.Color('green')
			behaviours.ReturnToGoal(drivebase,sensors.Values)

	# Stop motors and reset brick color 
	drivebase.Coast()
	brick.Color('green')

# Define all our buttons and functions
menu_buttons = [
	MenuButton("Run Program",script=main),
	MenuButton("Calibrate",script=calibration.Calibrate,args=[brick,drivebase,sensors]),
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