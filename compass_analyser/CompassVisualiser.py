#!/usr/bin/env python3

import json

import brick
import sensors
import drivebase

# sensors.calibration.CalibrateField(brick,drivebase,sensors)

sensors.calibration.goal_heading = 28

data = []

drivebase.Drive([1] * 4)

for i in range(400):
	sensors.UpdateValues()

	data.append({
		"Raw" : sensors.Values.raw_compass,
		"Heading" : sensors.Values.raw_compass - sensors.calibration.goal_heading,
		"Final" : sensors.Values.compass
	})

drivebase.Coast()

with open("compass.json","w") as file:
	json.dump(data,file)