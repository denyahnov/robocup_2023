#!/usr/bin/env python3

import RoboCup as rc
from RoboCup.Menu import Menu, MenuButton

from ev3dev2.motor import *
from ev3dev2.port import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *

import math
from time import sleep,time
from json import load,dump

class LowPassFilter():
	SAMPLE_RATE = 20

	def __init__(self,omega_c):
		self.init_constants(omega_c, 1 / LowPassFilter.SAMPLE_RATE)

		self.last_input = 0
		self.last_output = 0

	def init_constants(self,omega_c, T):
		self.alpha = (2 - T * omega_c) / (2 + T * omega_c)
		self.beta = T * omega_c / (2 + T * omega_c)

	def process_sample(self,x):
		y = self.alpha * self.last_output + self.beta * (x + self.last_input)

		self.last_input = x
		self.last_output = y

		return y

class SoccerRobot(rc.Robot):
	def __init__(self):
		"""What our class does when created (initialised)"""

		# Initialise rc.Robot class
		super().__init__() 

		# Define all our buttons and functions
		self.menu_buttons = [
			MenuButton("Run Program",script=self.RunProgram),
			MenuButton("Calibrate",script=self.calibrate),
			MenuButton("Debug: False",script=self.toggle_debug),
			MenuButton("Exit",script=self.close_menu),
		]

		# Create Menu Class
		self.menu = Menu([2,2],self.menu_buttons)

		# Setup our variables
		self.init_variables()

		# Load our calibration data
		self.read_calibration()

		# Setup sensors/motors
		self.init_ports()

		# Update UI to show debug status
		self.update_debug()

	def init_ports(self):
		"""Initialise all motors and sensors"""

		self.Port['A'] = MediumMotor(OUTPUT_A)
		self.Port['B'] = MediumMotor(OUTPUT_B)
		self.Port['C'] = MediumMotor(OUTPUT_C)
		self.Port['D'] = MediumMotor(OUTPUT_D)

		self.Port['2'] = Sensor(INPUT_2,driver_name=rc.Driver.COMPASS)
		self.Port['3'] = UltrasonicSensor(INPUT_3)

		self.Port['2'].mode = "COMPASS"


		if self.robot_id == 0:
			self.Port['1'] = rc.IRSeeker360(INPUT_1)
		else:
			self.Port['1'] = rc.DoubleInfrared(
				(INPUT_1, 0),
				(INPUT_4, 180),
			)

		self.BallFilter = LowPassFilter(10)

		self.PrintPorts()

	def init_variables(self):
		"""Create useful variables"""

		self.robot_id = 0
		self.debug_mode = False

		self.goal_heading = 0
		self.center_distance = 0

		self.sound_volume = 20

	def save_calibration(self):
		"""Save calibration data"""
		with open("calibration.json",'w') as file:
			dump({
				"robot_id": self.robot_id,
				"debug_mode": self.debug_mode,
				"goal_heading": self.goal_heading,
				"center_distance": self.center_distance,
			},file,indent=4)

	def read_calibration(self):
		"""Load calibration data"""
		try:
			with open("calibration.json",'r') as file:
				temp = load(file)

				self.robot_id = temp["robot_id"]
				self.debug_mode = temp["debug_mode"]
				self.goal_heading = temp["goal_heading"]
				self.center_distance = temp["center_distance"]

				del temp
		except FileNotFoundError:
			self.save_calibration()

	def calibrate(self):
		"""Calibrate all sensors, Reset motor positions and read goal heading + wall distance"""

		# Set brick color to orange
		self.Color('orange')

		#######################################

		# Reset Motors
		self.ResetMotors()

		self.Port['2'].command = "BEGIN-CAL"
		self.Port['2'].command = "END-CAL"

		# Reset Variables
		self.goal_heading = self.Port['2'].value()
		self.center_distance = self.Port['3'].distance_centimeters

		# Set sound volume
		self.Sound.set_volume(self.sound_volume)

		#######################################

		# Save the data to json file
		self.save_calibration()

		# Play beep to indicate calibration finished
		self.Sound.play_tone(650,0.3,0,20,self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

		# Reset brick color
		self.Color('green')

	def toggle_debug(self):
		"""Toggle debug state"""
		self.debug_mode = not self.debug_mode

		self.update_debug()

	def update_debug(self):
		"""Update Debug Button Text"""
		self.menu_buttons[2].text = "Debug: " + str(self.debug_mode)

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
			front_left, 	# Motor A
			back_left,		# Motor B
			front_right,	# Motor C
			back_right,		# Motor D
		]

	def Invert(self,speeds):
		return [
			-speeds[0],
			speeds[1],
			speeds[2],
			-speeds[3],
		]

	def ConvertAngle(self,value:float) -> float:
		"""Convert 0 to 360 degrees -> -180 to 180 degrees"""

		return value if value <= 180 else value - 360

	def RunProgram(self):
		"""Main loop"""

		# Change brick color to red
		self.Color('red')

		DEBUG = []

		while True:
			# Update button variables
			self.Buttons.process()

			# Stop program if middle or exit button pressed
			if self.Buttons.enter or self.Buttons.backspace: break

			# Unpack IR data
			ball_angle, ball_strength = self.Port['1'].read()

			# Compass Data
			compass = self.Port['2'].value()

			angle = self.ConvertAngle(ball_angle * 30)

			# Filter out ball angle
			filtered_angle = self.BallFilter.process_sample(angle)

			# Calculate the 4 motor speeds
			# Scale the speeds to our target speed
			scaled_speeds = self.ScaleSpeeds(50,self.CalculateMotors(filtered_angle))

			# Run the motors at desired speeds
			self.StartMotors(self.Invert(scaled_speeds))

			# Store data if we want to debug the robot
			if self.debug_mode:
				DEBUG.append([])

		# Stop motors and reset brick color 
		self.CoastMotors()
		self.Color('green')

		# Save debug data
		if self.debug_mode:
			with open("{}.json".format(round(time())),"w") as file:
				dump(DEBUG,file)

	def Begin(self):
		""" WHAT WE WANT TO CALL WHEN RUNNING CODE """

		# Beep to tell us the robot is ready
		self.Sound.play_tone(700,0.2,0,20,self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

		# Run the menu
		self.menu.Run()

		# Once finished reset motors and change color back to green
		self.CoastMotors()
		self.Color('green')

# If the program is started run the code
if __name__ == '__main__':
	robot = SoccerRobot()
	robot.Begin()