#!/usr/bin/env python3

import RoboCup as rc
from RoboCup.Menu import Menu, MenuButton

from ev3dev2.motor import *
from ev3dev2.port import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *

import math
from time import sleep

class SoccerRobot(rc.Robot):
	def __init__(self):
		"""What our class does when created (initialised)"""

		# Initialise rc.Robot class
		super().__init__() 

		# Define all our buttons and functions
		self.menu_buttons = [
			MenuButton("Run Program",script=self.RunProgram),
			MenuButton("Calibrate",script=self.calibrate),
			MenuButton("Connect Bluetooth"),
			MenuButton("Exit",script=self.close_menu),
		]

		# Create Menu Class
		self.menu = Menu([2,2],self.menu_buttons)

		# Setup our robot stuff
		self.init_ports()
		self.init_variables()
		self.calibrate()

	def init_ports(self):
		"""Initialise all motors and sensors"""

		self.Port['A'] = MediumMotor(OUTPUT_A)
		self.Port['B'] = MediumMotor(OUTPUT_B)
		self.Port['C'] = MediumMotor(OUTPUT_C)
		self.Port['D'] = MediumMotor(OUTPUT_D)

		self.Port['1'] = rc.IRSeeker360(INPUT_1)
		self.Port['2'] = Sensor(INPUT_2,driver_name=rc.Driver.COMPASS)
		self.Port['3'] = UltrasonicSensor(INPUT_3)

	def init_variables(self):
		"""Create useful variables"""

		self.goal_heading = 0
		self.center_distance = 0

		self.max_speed = 80
		self.min_speed = 30

		self.sound_volume = 20

	def calibrate(self,initiating=False):
		"""Calibrate all sensors, Reset motor positions and read goal heading + wall distance"""

		# Set brick color to orange
		self.Color('orange')

		#######################################

		# Reset Motors
		self.ResetMotors()

		# Reset Variables
		# self.goal_heading = self.Port['2'].read()
		# self.center_distance = self.Port['3'].distance_centimeters

		# Set sound volume
		self.Sound.set_volume(self.sound_volume)

		#######################################

		# Play beep to indicate calibration finished
		self.Sound.play_tone(650,0.3,0,20,self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

		# Reset brick color
		self.Color('green')

	def close_menu(self):
		"""Close program"""
		raise KeyboardInterrupt

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
			front_right, 	# Motor A
			back_right,		# Motor B
			front_left,		# Motor C
			back_left		# Motor D
		]

	def SmoothAngle(self, current, target, smoothing = 0.5, min_speed = 5):
		"""Smooth the transition from 2 angles"""

		diff = current - target

		while diff < -180: diff += 360
		while diff > 180: diff -= 360

		increase = abs(diff) * smoothing

		rtn = target - increase

		return rtn if rtn > min_speed else target

	def FixBallAngle(self,ball_angle:int) -> int:
		"""Convert IR angle to 360 degrees"""
		return ball_angle * (360/12)

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

			# Run the motors at desired speeds
			self.StartMotors(scaled_speeds)	

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