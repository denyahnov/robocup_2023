#!/usr/bin/env python3

#import time

#from timeit import repeatm
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
import time

#IMPORT MOTORS
Leftmotor = MediumMotor(OUTPUT_A)
Rightmotor = MediumMotor(OUTPUT_B)
Bottommotor = MediumMotor(OUTPUT_C)
Topmotor = MediumMotor(OUTPUT_D)



#Move in a Square
Rightmotor.on_for_seconds(25,200, block=False)
Leftmotor.on_for_seconds(0,200, block=False)
Topmotor.on_for_seconds(100,200, block=False)
Bottommotor.on_for_seconds(50,200, block=False)