#!/usr/bin/env python3

"""
	A \\__// C
	
   Left		Right

	B  Back  D

Front IR 	1
Compass 	2
Ultrasonic	3
Back IR 	4
			
"""

import brick
import comms
import behaviours

from menu import Menu, MenuButton

# Handle Import Errors (Cable Not Connected)
try:
	import drivebase
	import sensors
except Exception as error:

	empty_menu = Menu([1,1],[])

	brick.Color('red')

	empty_menu.Print(str(error),line_length=25)

	while not brick.buttons.backspace:
		brick.buttons.process()

	brick.Color('green')

	exit(error)

def main():
	"""Main loop"""

	sensors.Values.robot_running = True

	kickoff_length = 20

	for _ in range(kickoff_length):
		behaviours.Kickoff(drivebase,sensors.Values)

	while True:

		# Update button variables
		brick.buttons.process()

		# Stop program if middle or exit button pressed
		if brick.buttons.enter or brick.buttons.backspace: break

		sensors.UpdateValues()


		if comms.state == comms.State.CONNECTED:

			if sensors.Values.has_ball:
				behaviours.Chase(drivebase,sensors.Values)
			
			elif sensors.Values.found_ball:
				if comms.other_data["state"] and comms.other_data["has_ball"]:
					behaviours.ReturnToGoal(drivebase,sensors.Values)
	
				else:
					behaviours.Chase(drivebase,sensors.Values)

			else:
				behaviours.ReturnToGoal(drivebase,sensors.Values)

		else:

			# If we have the ball long enough, try score
			if sensors.Values.has_ball:
				behaviours.Chase(drivebase,sensors.Values)
			
			# Otherwise if we can see the ball, chase it
			elif sensors.Values.found_ball:
				behaviours.Chase(drivebase,sensors.Values)

			# If we cannot find the ball, wait	
			else:
				behaviours.ReturnToGoal(drivebase,sensors.Values)

	sensors.Values.robot_running = False

	# Stop motors and reset brick color 
	drivebase.Coast()
	brick.Color('green')

# Define all our buttons and functions
menu_buttons = [
	MenuButton("Run Program",script=main),
	MenuButton("Calibrate Field",script=sensors.calibration.CalibrateField,args=[brick,drivebase,sensors]),
	MenuButton("Calibrate Ball",script=sensors.calibration.CalibrateBall,args=[brick,sensors]),
	MenuButton("Bluetooth",script=comms.Connect,args=[brick,sensors]),
]

# Create Menu Class
menu = Menu([2,2], menu_buttons)

# Get Bluetooth Address using `robot_id`
comms.InitComms(sensors.calibration)

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