#!/usr/bin/env python3

import RoboCup as rc
from RoboCup.Menu import Menu, MenuButton

from ev3dev2.motor import *
from ev3dev2.port import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *

import math
from time import sleep
from json import load,dump

class SoccerRobot(rc.Robot):
	def __init__(self):
		"""What our class does when created (initialised)"""

		# Initialise rc.Robot class
		super().__init__() 

		# Define all our buttons and functions
		self.menu_buttons = [
			MenuButton("Run Program",script=self.RunProgram),
			MenuButton("Calibrate",script=self.calibrate),
			MenuButton("Testing",script=self.Testing),
			MenuButton("Exit",script=self.close_menu),
		]

		# Create Menu Class
		self.menu = Menu([2,2],self.menu_buttons)

		# Setup our robot stuff
		self.init_ports()
		self.init_variables()

		# Load our calibration data
		self.read_calibration()

	def init_ports(self):
		"""Initialise all motors and sensors"""

		self.Port['A'] = MediumMotor(OUTPUT_A)
		self.Port['B'] = MediumMotor(OUTPUT_B)
		self.Port['C'] = MediumMotor(OUTPUT_C)
		self.Port['D'] = MediumMotor(OUTPUT_D)

		self.Port['1'] = rc.IRSeeker360(INPUT_1)
		self.Port['2'] = Sensor(INPUT_2,driver_name=rc.Driver.COMPASS)
		# self.Port['3'] = UltrasonicSensor(INPUT_3)

		self.Port['2'].mode = "COMPASS"

	def init_variables(self):
		"""Create useful variables"""

		self.goal_heading = 0
		self.center_distance = 0

		self.max_speed = 80
		self.min_speed = 30

		self.sound_volume = 20

	def save_calibration(self):
		"""Save calibration data"""
		with open("calibration.json",'w') as file:
			dump({
				"goal_heading": self.goal_heading,
				"center_distance": self.center_distance,
			},file,indent=4)

	def read_calibration(self):
		"""Load calibration data"""
		try:
			with open("calibration.json",'r') as file:
				temp = load(file)

				self.goal_heading = temp["goal_heading"]
				self.center_distance = temp["center_distance"]

				del temp
		except FileNotFoundError:
			self.save_calibration()

	def calibrate(self,initiating=False):
		"""Calibrate all sensors, Reset motor positions and read goal heading + wall distance"""

		# Set brick color to orange
		self.Color('orange')

		#######################################

		# Reset Motors
		self.ResetMotors()

		# Reset Variables
		self.goal_heading = self.Port['2'].value()
		# self.center_distance = self.Port['3'].distance_centimeters

		# Set sound volume
		self.Sound.set_volume(self.sound_volume)

		#######################################

		# Save the data to json file
		self.save_calibration()

		# Play beep to indicate calibration finished
		self.Sound.play_tone(650,0.3,0,20,self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

		# Reset brick color
		self.Color('green')

	def close_menu(self):
		"""Close program"""
		raise KeyboardInterrupt

	def Turn(self,motors:list,speed:float) -> list:
		"""Turn our robot at a certain speed"""
		return [motor + speed for motor in motors]

	def CalculateMotors(self,angle:float) -> list:
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
			back_left,		# Motor B
			front_right,	# Motor C
			back_right,		# Motor D
		]

	def PointTo(self,target:float,current:float) -> float:
		"""Turn until we reach the target"""

		return -self.Speed.Clamp((self.ConvertCompass(current - target) + 4) / 3.5)

	def FixBallAngle(self,ball_angle:int) -> int:
		"""Convert IR angle to 360 degrees"""

		return ball_angle * (360/12)

	def Inverse(self,motors:list) -> list:
		"""Inverse certain motors"""

		return [-motors[0],motors[1],motors[2],-motors[3]]

	def ConvertCompass(self,value:float) -> float:
		"""Convert 0 to 360 degrees -> -180 to 180 degrees"""

		return value if value <= 180 else value - 360

	def GetRobotPosition(self,angle:float,distance:float) -> tuple:
		"""Get Robot x,y position relative to the ball at (0,0)"""

		return (distance * math.cos(angle + 90),-distance * math.sin(angle + 90))

	def Testing(self):
		"""Testing ENV"""

		# Change brick color to red
		self.Color('red')

		target_angle = 0

		current_angle = target_angle
		current_speed = 100

		while True:
			# Update button variables
			self.Buttons.process()

			# Stop program if middle or exit button pressed
			if self.Buttons.enter or self.Buttons.backspace: break

			# Unpack IR data
			ball_angle, ball_strength = self.Port['1'].read()

			# Get our target angle (towards the ball)
			target_angle = self.FixBallAngle(ball_angle)

			# Calculate the 4 motor speeds
			motor_calc = self.CalculateMotors(target_angle)

			# Scale the 4 speeds to our target speed
			scaled_speeds = self.ScaleSpeeds(current_speed,motor_calc)

			# Run the motors at desired speeds
			self.StartMotors(self.Inverse(scaled_speeds))

			# Debugging stuff
			print("\nBall Angle:",ball_angle)
			print("Ball Strength:",ball_strength)
			print("Fixed Angle",target_angle)

		# Stop motors and reset brick color 
		self.CoastMotors()
		self.Color('green')


	def RunProgram(self):
		"""Main loop"""

		# Change brick color to red
		self.Color('red')

		target_angle = 0

		current_angle = target_angle
		current_speed = self.max_speed

		while True:
			# Update button variables
			self.Buttons.process()

			# Stop program if middle or exit button pressed
			if self.Buttons.enter or self.Buttons.backspace: break

			# Unpack IR data
			ball_angle, ball_strength = self.Port['1'].read()

			# Get our target angle (towards the ball)
			target_angle = self.FixBallAngle(ball_angle)

			# Update our current angle
			current_angle = self.SmoothAngle(current_angle,target_angle)

			# Calculate the 4 motor speeds
			motor_calc = self.CalculateMotors(current_angle)

			# Scale the 4 speeds to our target speed
			scaled_speeds = self.ScaleSpeeds(current_speed,motor_calc)

			# Calculate our goal heading curve
			compass_fix = self.PointTo(self.goal_heading, self.Port['2'].value())

			# Turn to goal
			curved_speeds = self.Turn(scaled_speeds, compass_fix)

			# Run the motors at desired speeds
			self.StartMotors(self.Inverse(curved_speeds))	

			# Debugging stuff
			print("\nBall Angle:",ball_angle)
			print("Ball Strength:",ball_strength)
			print("Fixed Angle",target_angle)

		# Stop motors and reset brick color 
		self.CoastMotors()
		self.Color('green')

	def Begin(self):
		""" WHAT WE WANT TO CALL WHEN RUNNING CODE """

		# Run the menu
		self.menu.Run()

		# Once finished reset motors and change color back to green
		self.CoastMotors()
		self.Color('green')

# If the program is started run the code
if __name__ == '__main__':
	robot = SoccerRobot()
	robot.Begin()