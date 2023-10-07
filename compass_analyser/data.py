import json

with open("compass.json","r") as file:
	data = json.load(file)

import matplotlib.pyplot as plt

a,b,c = zip(*[(d["Raw"],d["Heading"],d["Final"]) for d in data])

d,e,f = [180] * len(data), [-180] * len(data), [360] * len(data)

new = [i % 360 for i in b]
new2 = [i % 360 for i in b]

fig, ax = plt.subplots()

# ax.plot(a,label="raw")
# ax.plot(b,label="head")
ax.plot(c,label="final")
# ax.plot(new,label="new")

ax.plot(d)
ax.plot(e)
# ax.plot(f)

leg = plt.legend(loc='upper center')

plt.show()