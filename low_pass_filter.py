# import json file
import json
import os

FILE_NAME = "1586594900.7226837.json"

with open("DEBUG\\" + FILE_NAME,"r") as file:
    vals = json.load(file)
    vals = [(v[-3] if v[-3] <= 180 else v[-3] - 360) for v in vals]


out = [0 for i in range(len(vals))]

print(min(vals), max(vals))

# how many ticks your robot runs at per second
sample_rate = 16

# initialise this before robot starts
def init_constants(omega_c, T):
    alpha = (2 - T * omega_c) / (2 + T * omega_c)
    beta = T * omega_c / (2 + T * omega_c)
    return alpha, beta

# call this every time you receive a heading from the ir sensor about where the ball is
def process_sample(x, x_prev, y, alpha, beta):
    y = alpha * y + beta * (x + x_prev)
    return y



alpha, beta = init_constants(12, 1/sample_rate)





for i in range(len(vals)):
    if i == 0:
        out[i] = vals[i]
    else:
        out[i] = process_sample(vals[i], vals[i - 1], out[i - 1], alpha, beta)