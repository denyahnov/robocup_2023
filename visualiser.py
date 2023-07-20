import GameMaker as gm
from GameMaker.Assets import *

import math
import json

FILE_NAME = "1586594900.7226837.json"

def ClampList(values: list,min_value=-100,max_value=100) -> list:
	clamped = [None] * len(values)

	for i,value in enumerate(values):
		if value < min_value: value = min_value
		if value > max_value: value = max_value

		clamped[i] = value

	return clamped

def AngleToPosition(angle,distance):
	return distance * math.cos(math.radians(angle - 90)), distance * math.sin(math.radians(angle - 90))

with open("DEBUG\\" + FILE_NAME,"r") as file:
	data = json.load(file) 

window = gm.Window([400,400],fps=20)

tick = 0

def speed_to_color(speed):
	if speed > 0:
		return [30,speed * 2,30]
	else:
		return [speed * -2,30,30]

class Robot():
	MotorW,MotorH = 25,50

	Body = Rectangle([150,150,100,100])
	Motors = [
		RotatedRectangle([125 + MotorW / 2, 125, MotorW, MotorH],rotation=315),
		RotatedRectangle([225 + MotorW / 2, 125, MotorW, MotorH],rotation=45),
		RotatedRectangle([225 + MotorW / 2, 225, MotorW, MotorH],rotation=135),
		RotatedRectangle([125 + MotorW / 2, 225, MotorW, MotorH],rotation=225),
	]
	Ball = Ellipse([0,0,30,30],width=2,color=(255,0,0))

	Speeds = [0,0,0,0]

while window.RUNNING:
	ball_angle, target_angle, filtered_angle = data[tick][-3:]

	x1,y1 = AngleToPosition(target_angle,60)
	x2,y2 = AngleToPosition(ball_angle,80)
	x3,y3 = AngleToPosition(filtered_angle,100)

	Robot.Speeds = ClampList(data[tick][0])

	for i,Motor in enumerate(Robot.Motors):
		Motor.foreground_color = speed_to_color(Robot.Speeds[i])

	window.draw(Line([200,200,200 + x3, 200 + y3],color=(0,255,0)))
	window.draw(Line([200,200,200 + x2, 200 + y2],color=(255,0,0)))
	window.draw(Line([200,200,200 + x1, 200 + y1],color=(0,0,255)))

	window.draw(Text(tick,[10,10]),gm.GUI)

	window.draw([Robot.Body] + Robot.Motors, gm.BACKGROUND)

	window.update()

	tick += 1

	if tick == len(data):
		window.RUNNING = False