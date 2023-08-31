#!/usr/bin/env python3

from ev3dev2.display import Display
from ev3dev2.button import Button

import sensors

display = Display()
buttons = Button()

def Draw(lines):
	display.clear()

	for i, line in enumerate(lines):
		display.text_pixels(str(line),clear_screen=False,y=i*10,x=0)	
		display.text_pixels(str(lines[line]),clear_screen=False,y=i*10,x=120)	

	display.update()

def CalibratedValues(values):

	ball_angle, ball_strength = values["Ball Angle: "], values["Ball Strength: "]

	return {
		"Near Strength (%s)" % sensors.NEAR_STRENGTH: ball_strength >= sensors.NEAR_STRENGTH,
		"Hold Strength (%s)" % sensors.HOLD_STRENGTH: ball_strength >= sensors.HOLD_STRENGTH,
		"Hold Angle (%s)" % sensors.HOLD_ANGLE: sensors.HOLD_ANGLE >= ball_angle >= -sensors.HOLD_ANGLE,
	}

def GetValues():
	
	ball_direction, ball_strength = sensors.IR.read()
	
	ball_angle = sensors.ConvertAngle(ball_direction * 30)


	return {
		"Ball Direction: ": ball_direction,
		"Ball Angle: ": ball_angle,
		"Ball Strength: ": ball_strength,
	}

if __name__ == '__main__':
	while not buttons.backspace:
		
		buttons.process()

		values = GetValues()

		calibrated = CalibratedValues(values)

		values.update(calibrated)

		Draw(values)