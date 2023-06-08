import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import json

with open("debug.txt","r") as file:
	data = json.load(file) 

data = data[100:180]

print(len(data))

fig, ax = plt.subplots()

def SmoothAngle(current:float, target:float, smoothing:float = 0.5, min_speed:float = 3):
	"""Smooth the transition from 2 angles"""

	diff = current - target

	while diff < -180: diff += 360
	while diff > 180: diff -= 360

	increase = abs(diff) * smoothing

	rtn = target - increase

	return rtn if rtn > min_speed else target

ax.plot(range(len(data)), [d[0] for d in data], label = "Ball Angle")

for i in range(len(data)-1):
	data[i+1][0] = SmoothAngle(data[i][0],data[i+1][0]) 

# ax.plot(range(len(data)), [d[1] for d in data], label = "Target Angle")
# ax.plot(range(len(data)), [d[2] for d in data], label = "Current Angle")

ax.plot(range(len(data)), [d[0] for d in data], label = "Smoothed")

# ax.plot(range(len(data)), [d[0][0] for d in data], label='Motor A')
# ax.plot(range(len(data)), [d[0][1] for d in data], label='Motor B')
# ax.plot(range(len(data)), [d[0][2] for d in data], label='Motor C')
# ax.plot(range(len(data)), [d[0][3] for d in data], label='Motor D')
# ax.plot(range(len(data)), [d[2] for d in data], label='Direction')

plt.legend()

plt.show()