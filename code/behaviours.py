
# BEHAVIOUR HELPERS

def GetDirection(values):
	"""Calculate Robot Chase Direction"""
	
	# Angle: Close, Far

	return {
		"0":  [0,0],

		"30": [50,35],
		"60": [115,65],
		"90": [150,115],
		"120": [205,125],
		"150": [255,155],
		"180": [305,185],
		
		"-30": [-50,-35],
		"-60": [-115,-65],
		"-90": [-150,-115],
		"-120": [-205,-125],
		"-150": [-255,-155],
		"-180": [-305,-185],
	}[str(values.ball_angle)][int(not values.near_ball)]

def FixCompass(drivebase,values,speeds) -> list:
	return drivebase.Turn(speeds, drivebase.TurnToHeading(values.compass))


# ROBOT BEHAVIOURS

def Score(drivebase,values):
	"""Same as `Chase` except it faces the goal"""
	
	# If near ball, drive behind it instead of into it
	angle = GetDirection(values)

	if (-30 <= angle <= 30) or (angle <= -150) or (angle >= 150): 
		drivebase.DriveSpeed.SPEED = drivebase.DriveSpeed.FAST
	elif (50 <= angle <= 105) or (-50 >= angle >= -105) and values.near_ball:
		drivebase.DriveSpeed.SPEED = drivebase.DriveSpeed.SLOW
	else:
		drivebase.DriveSpeed.SPEED = drivebase.DriveSpeed.NORMAL

	# Calculate 4 motor speeds
	speeds = drivebase.ScaleSpeeds(drivebase.MoveTo(angle))
	
	# Turn to fix compass
	turned_speeds = drivebase.Turn(speeds, drivebase.TurnToHeading(values.ultrasonic / 2.5))

	# Start motors
	return drivebase.Drive(turned_speeds)

def Chase(drivebase,values):
	"""Drive towards the ball and face 0 degrees"""

	# If near ball, drive behind it instead of into it
	angle = GetDirection(values)

	if (-30 <= angle <= 30) or (angle <= -150) or (angle >= 150): 
		drivebase.DriveSpeed.SPEED = drivebase.DriveSpeed.FAST
	elif (50 <= angle <= 105) or (-50 >= angle >= -105) and values.near_ball:
		drivebase.DriveSpeed.SPEED = drivebase.DriveSpeed.SLOW
	else:
		drivebase.DriveSpeed.SPEED = drivebase.DriveSpeed.NORMAL

	# Calculate 4 motor speeds
	speeds = drivebase.ScaleSpeeds(drivebase.MoveTo(angle))
	
	# Turn to fix compass
	turned_speeds = FixCompass(drivebase,values,speeds)

	# Start motors
	return drivebase.Drive(turned_speeds)

def Track(drivebase,values):
	"""Turn to face the ball but don't drive towards it"""
	
	speeds = [0,0,0,0]

	# Turn to ball face angle
	return drivebase.Drive(drivebase.Turn(speeds, drivebase.TurnToHeading(values.ball_angle)))

def Defend(drivebase,values):
	"""Goalie Logic"""

	# If ball is far away, just track it
	if values.ball_strength < 60:
		Track(drivebase,values)

	# Otherwise attack the ball
	else:
		Chase(drivebase,values)

def ReturnToGoal(drivebase,values):
	"""Return to Goal using ultrasonic and touch sensor"""
	
	# If robot is stuck on back wall
	if drivebase.IsStalled():
		return drivebase.DriveSeconds(0.5,drivebase.ScaleSpeeds(drivebase.MoveTo(0)))

	# If not centered
	if not (-10 < values.ultrasonic < 10):
		return RecenterRobot(drivebase,values)

	if abs(values.last_ultrasonic - values.ultrasonic) > 50:
		# Drive forwards if we reach the goal (large ultrasonic change)
		return drivebase.DriveSeconds(0.2,drivebase.ScaleSpeeds(drivebase.MoveTo(0)))

	# Drive backwards
	return drivebase.Drive(drivebase.ScaleSpeeds(drivebase.MoveTo(180)))

def RecenterRobot(drivebase,values):
	"""Recenter the robot's x position using ultrasonic"""

	# Calculate 4 motor speeds
	if values.ultrasonic < -10:
		speeds = drivebase.ScaleSpeeds(drivebase.MoveTo(90))
	elif values.ultrasonic > 10:
		speeds = drivebase.ScaleSpeeds(drivebase.MoveTo(-90))
	else:
		speeds = [0,0,0,0]

	# Turn to fix compass
	turned_speeds = FixCompass(drivebase,values,speeds)

	# Start motors
	return drivebase.Drive(turned_speeds)

def Idle(drivebase,values):
	"""Face 0 degrees and wait"""
	speeds = [0,0,0,0]

	# Turn to heading 0
	return drivebase.Drive(FixCompass(drivebase,values,speeds))

def Kickoff(drivebase,values):
	# Go straight ahead during kickoff

	speeds = drivebase.ScaleSpeeds(drivebase.MoveTo(0))

	turned = drivebase.ScaleSpeeds(FixCompass(drivebase,values,speeds))

	# Drive at angle 0
	return drivebase.Drive(turned)