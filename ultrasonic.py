import math

def CalcDistanceOffset(target,angle):
	return target / math.cos(math.radians(angle if abs(angle) <= 50 else 50))

print(
	CalcDistanceOffset(100,90)
)