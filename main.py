#!/usr/bin/env python3

import RoboCup as rc
from RoboCup.Menu import Menu, MenuButton

from ev3dev2.motor import *

import math
from time import sleep

class SoccerRobot(rc.Robot):
    def __init__(self):
        super().__init__()

        self.menu_buttons = [
            MenuButton("Run Program",script=self.RunProgram),
            MenuButton("Calibrate",script=self.calibrate),
            MenuButton("Connect Bluetooth"),
            MenuButton("Exit",script=self.close_menu),
        ]

        self.menu = Menu([2,2],self.menu_buttons)

        self.x, self.y = 0,0

        self.init_ports()
        self.calibrate()

    def init_ports(self):
        self.Port['A'] = MediumMotor(OUTPUT_A)
        self.Port['B'] = MediumMotor(OUTPUT_B)
        self.Port['C'] = MediumMotor(OUTPUT_C)
        self.Port['D'] = MediumMotor(OUTPUT_D)

    def calibrate(self,initiating=False):
        self.Color('orange')

        self.ResetMotors()

        self.Sound.set_volume(20)

        self.Sound.play_tone(650,0.3,0,20,self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

        self.Color('green')

    def close_menu(self):
        raise KeyboardInterrupt

    def CalculateMotors(self,angle:float) -> list:
        angle = math.radians(angle)

        fl =  1 * math.cos(math.pi / 4 - angle)
        fr = -1 * math.cos(math.pi / 4 + angle)
        bl =  1 * math.cos(math.pi / 4 + angle)
        br = -1 * math.cos(math.pi / 4 - angle)

        return [fr,br,fl,bl]

    def RunProgram(self):
        self.Color('red')

        angle = 0
        speed = 100
        increment = 3

        while True:
            self.Buttons.process()

            if self.Buttons.enter: break

            angle += increment

            speeds = self.CalculateMotors(angle)

            scaled_speeds = self.ScaleSpeeds(self.Speed.Clamp(speed),speeds)

            self.StartMotors(scaled_speeds)

        self.CoastMotors()
        self.Color('green')

    def Begin(self):
        self.menu.Run()

        self.CoastMotors()
        self.Color('green')

if __name__ == '__main__':
    robot = SoccerRobot()
    robot.Begin()