def SmoothAngle(current, target, smoothing = 0.4, min_speed = 5):
	"""Smooth the transition from 2 angles"""

	diff = current - target

	while diff < -180: diff += 360
	while diff > 180: diff -= 360

	increase = diff * smoothing * -1

	rtn = target - increase

	print(abs(diff))
	print(increase)
	print(rtn)

	return rtn if rtn > min_speed else target

import random

x,y = random.randint(0,360),random.randint(0,360)
print((x,y))
SmoothAngle(x,y)

