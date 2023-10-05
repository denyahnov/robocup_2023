#!/usr/bin/env python3

from time import sleep
from json import dump, load

# GREEN ROBOT 	= ID 0
# MULTICOLOR 	= ID 1

global robot_id, goal_heading, center_distance, ball_strengths

robot_id, goal_heading, center_distance = 0,0,0

ball_strengths = [[0,0] for _ in range(12)]

"""
Ball Calibration Button Guide
	 ______
	//NEAR\\	UP
	========
	________
	| SAVE |	MIDDLE
	========
	________
	\\HOLD//	DOWN
	========

	MIDDLE = SAVE AND EXIT
	BACKSPACE = SAVE WITHOUT EXITING
"""

def Save():
	"""Save calibration data"""
	global robot_id, goal_heading, center_distance, ball_strengths
	
	with open("calibration.json",'w') as file:
		dump({
			"robot_id": robot_id,
			"goal_heading": goal_heading,
			"center_distance": center_distance,
			"ball_strengths": ball_strengths,
		},file,indent=4)

def Load():
	"""Load calibration data"""
	global robot_id, goal_heading, center_distance, ball_strengths
	
	try:
		with open("calibration.json",'r') as file:
			temp = load(file)

			robot_id = temp["robot_id"]
			goal_heading = temp["goal_heading"]
			center_distance = temp["center_distance"]
			ball_strengths = temp["ball_strengths"]

	except FileNotFoundError:
		Save()

def CalibrateCompass(brick,drivebase,sensors):
	global goal_heading

	brick.Color('orange')

	# Use Compass graph to find most accurate heading
	goldilocks_heading = 50

	while not brick.buttons.enter:
		compass = sensors.ConvertAngle((sensors.Compass.value() - goldilocks_heading) % 360)

		drivebase.Drive(drivebase.Turn([0,0,0,0],drivebase.TurnToHeading(compass)), scale_speeds=False)

		if -1 <= compass <= 1:
			brick.PlayTone(600,time=0.5)

	drivebase.Coast()

	brick.Color('green')

def CalibrateField(brick,drivebase,sensors):
	"""Calibrate all sensors, Reset motor positions and read goal heading + wall distance"""

	global goal_heading, center_distance

	brick.Color('orange')

	drivebase.Reset()

	sensors.Compass.command = "BEGIN-CAL"
	sensors.Compass.command = "END-CAL"

	# Reset Variables
	goal_heading = sensors.Compass.value()
	center_distance = sensors.Ultrasonic.distance_centimeters

	# Save the data to json file
	Save()

	brick.Color('green')
	brick.PlayTone(650)

def DrawButtons(brick,direction,strength):

	X, Y = brick.display.xres, brick.display.yres

	xsize = 30
	ysize = 15
	xstretch = 15
	ystretch = 22

	b_xsize = 24
	b_ysize = 20

	top = [(X/2 - xsize, Y - ysize),(X/2 + xsize, Y - ysize),(X/2 + xsize + xstretch, Y - ysize - ystretch),(X/2 - xsize - xstretch, Y - ysize - ystretch)]
	bottom = [(X/2 - xsize, ysize),(X/2 + xsize, ysize),(X/2 + xsize + xstretch, ysize + ystretch),(X/2 - xsize - xstretch, ysize + ystretch)]

	middle = [(X/2 - b_xsize, Y/2 - b_ysize),(X/2 + b_xsize, Y/2 - b_ysize),(X/2 + b_xsize, Y/2 + b_ysize),(X/2 - b_xsize, Y/2 + b_ysize)]

	for button in [top,bottom,middle]:
		for i in range(len(button)):
			brick.display.draw.line(xy=[button[i-1],button[i]],width=3)

	brick.display.draw.rectangle(xy=[0,0,30,15],outline='black')
	brick.display.text_pixels("EXIT", clear_screen=False, x=3, y=3)

	text_x,text_y = 10,6

	brick.display.text_pixels("NEAR", clear_screen=False, x=X/2 - text_x, y=Y * 0.20 - text_y)
	brick.display.text_pixels("SAVE", clear_screen=False, x=X/2 - text_x, y=Y * 0.50 - text_y)
	brick.display.text_pixels("HOLD", clear_screen=False, x=X/2 - text_x, y=Y * 0.80 - text_y)

	brick.display.text_pixels("Direction:", clear_screen=False, x=0, y=Y/2 - text_y * 2)
	brick.display.text_pixels("Strength:", clear_screen=False, x=X/2 + 35, y=Y/2 - text_y * 2)

	brick.display.text_pixels(str(direction), clear_screen=False, x=X/2 - 65, y=Y/2)
	brick.display.text_pixels(str(strength), clear_screen=False, x=X/2 + 55, y=Y/2)

def CalibrateBall(brick,sensors):
	"""Read ball strength data and save to file"""

	global ball_strengths
	
	brick.Color('orange')
	
	try:
		while True:

			sensors.UpdateValues()

			direction, strength = sensors.Values.ball_direction, sensors.Values.ball_strength

			if brick.buttons.backspace: 
				raise KeyboardInterrupt

			if brick.buttons.enter: # SAVE
				
				while brick.buttons.enter:
					brick.buttons.process()
					sleep(0.01)

				Save()

				brick.PlayTone(650)

				break

			if brick.buttons.down: # HOLD
				
				while brick.buttons.down:
					brick.buttons.process()
					sleep(0.01)

				ball_strengths[direction][0] = strength

				brick.PlayTone(700,0.1)

			if brick.buttons.up: # NEAR
				
				while brick.buttons.up:
					brick.buttons.process()
					sleep(0.01)

				ball_strengths[direction][1] = strength

				brick.PlayTone(700,0.1)

			brick.display.clear()

			DrawButtons(brick,direction,strength)

			brick.display.update()

			brick.buttons.process()

			# brick.buttons.wait_for_released(brick.buttons.buttons_pressed)
		
	except KeyboardInterrupt:
		brick.display.clear()
		brick.display.update()
	
		print("Closed")

	brick.Color('green')

# == LOAD CALIBRATION DATA == #

Load()

# =========================== #