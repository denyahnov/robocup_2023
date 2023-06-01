import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import json

with open("debug.txt","r") as file:
	data = json.load(file) 

data = data[500:600]

fig, ax = plt.subplots()

ax.plot(range(len(data)), [d[0][0] for d in data], label='Motor A')
# ax.plot(range(len(data)), [d[0][1] for d in data], label='Motor B')
# ax.plot(range(len(data)), [d[0][2] for d in data], label='Motor C')
# ax.plot(range(len(data)), [d[0][3] for d in data], label='Motor D')
ax.plot(range(len(data)), [d[2] for d in data], label='Direction')

plt.legend()

plt.show()