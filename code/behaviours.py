
# BEHAVIOUR HELPERS

def FixCompass(drivebase,values,speeds) -> list:
	return drivebase.Turn(speeds, drivebase.TurnToHeading(values.compass))


# ROBOT BEHAVIOURS

def Score(drivebase,values):
	"""Same as `Chase` except it faces the goal"""
	
	# If near ball, drive behind it instead of into it
	if values.near_ball:
		angle = values.ball_angle * 1.6

	else:
		angle = values.ball_angle

	# Calculate 4 motor speeds
	speeds = drivebase.ScaleSpeeds(drivebase.MoveTo(angle))
	
	# Turn to fix compass
	turned_speeds = drivebase.Turn(speeds, drivebase.TurnToHeading(values.compass - values.ultrasonic / 8))

	# Start motors
	return drivebase.Drive(drivebase.ScaleSpeeds(turned_speeds))

def Chase(drivebase,values):
	"""Drive towards the ball and face 0 degrees"""

	# If near ball, drive behind it instead of into it
	if values.near_ball:
		angle = values.ball_angle * 1.6

	else:
		angle = values.ball_angle

	# Calculate 4 motor speeds
	speeds = drivebase.ScaleSpeeds(drivebase.MoveTo(angle))
	
	# Turn to fix compass
	turned_speeds = FixCompass(drivebase,values,speeds)

	# Start motors
	return drivebase.Drive(drivebase.ScaleSpeeds(turned_speeds))

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
	if not (-15 < values.ultrasonic < 15):
		return RecenterRobot(drivebase,values)

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