import GameMaker as gm
from GameMaker.Assets import *

import math
import json

def AngleToPosition(angle,distance):
	return distance * math.cos(math.radians(angle - 90)), distance * math.sin(math.radians(angle - 90))

with open("debug.txt","r") as file:
	data = json.load(file) 

window = gm.Window([400,400],fps=20)

tick = 0

while window.RUNNING:
	ball_angle, target_angle, current_angle = data[tick]

	x1,y1 = AngleToPosition(ball_angle,100)
	x2,y2 = AngleToPosition(target_angle,100)
	x3,y3 = AngleToPosition(current_angle,100)

	window.draw(Line([200,200,200 + x3, 200 + y3],color=(0,0,255)))
	window.draw(Line([200,200,200 + x2, 200 + y2],color=(0,255,0)))
	window.draw(Line([200,200,200 + x1, 200 + y1],color=(255,0,0)))

	window.draw(Text(tick,[10,10]))

	window.update()

	tick += 1

	if tick == len(data):
		window.RUNNING = False