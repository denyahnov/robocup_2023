import GameMaker as gm
from GameMaker.Assets import *

import math
import json

import low_pass_filter

def AngleToPosition(angle,distance):
	return distance * math.cos(math.radians(angle - 90)), distance * math.sin(math.radians(angle - 90))

def ScaleSpeeds(target_value:int,speeds:list) -> list:
	greatest = max([abs(speed) for speed in speeds])

	if greatest > target_value: greatest = target_value

	fix = target_value / greatest

	for i in range(len(speeds)):
		speeds[i] = int(round(speeds[i] * fix,2))

	return speeds

def CalculateMotors(angle:float) -> list:
	"""Calculate 4 Motor speeds from an angle"""
	angle = math.radians(angle)

	# Math stuff
	front_left =  -1 * math.cos(math.pi / 4 - angle)
	front_right = 1 * math.cos(math.pi / 4 + angle)
	back_left =  -1 * math.cos(math.pi / 4 + angle)
	back_right = 1 * math.cos(math.pi / 4 - angle)

	# Returns the speeds in [A,B,C,D] form
	return [
		front_left, 	# Motor A
		front_right,	# Motor C
		back_left,		# Motor B
		back_right,		# Motor D
	]

with open("debug.txt","r") as file:
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
	ball_angle, target_angle, current_angle = data[tick]

	x1,y1 = AngleToPosition(target_angle,60)
	x2,y2 = AngleToPosition(ball_angle,80)
	x3,y3 = AngleToPosition(low_pass_filter.out[tick],100)

	Robot.Speeds = ScaleSpeeds(100,CalculateMotors(low_pass_filter.out[tick]))

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