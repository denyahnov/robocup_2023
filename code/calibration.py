from json import dump, load

global robot_id, debug_mode, goal_heading, center_distance

robot_id, debug_mode, goal_heading, center_distance = 0,0,0,0

def Save():
	"""Save calibration data"""
	global robot_id, debug_mode, goal_heading, center_distance
	
	with open("calibration.json",'w') as file:
		dump({
			"robot_id": robot_id,
			"debug_mode": debug_mode,
			"goal_heading": goal_heading,
			"center_distance": center_distance,
		},file,indent=4)

def Load(self):
	"""Load calibration data"""
	global robot_id, debug_mode, goal_heading, center_distance
	
	try:
		with open("calibration.json",'r') as file:
			temp = load(file)

			robot_id = temp["robot_id"]
			debug_mode = temp["debug_mode"]
			goal_heading = temp["goal_heading"]
			center_distance = temp["center_distance"]

	except FileNotFoundError:
		Save()

def Calibrate(drivebase,sensors):
	"""Calibrate all sensors, Reset motor positions and read goal heading + wall distance"""

	global goal_heading, center_distance

	drivebase.Reset()

	sensors.Compass.command = "BEGIN-CAL"
	sensors.Compass.command = "END-CAL"

	# Reset Variables
	goal_heading = sensors.Compass.value()
	center_distance = sensors.Ultrasonic.distance_centimeters

	# Save the data to json file
	Save()