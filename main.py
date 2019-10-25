#!/usr/bin/env python3
from ev3dev2.motor import Motor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import ev3dev2.button
import time
import sys
import random

#The say function
sound = Sound()
def say(string): 
    while True:
        sound.speak(string)

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)

#Initialize the two large motors
#left_motor = LargeMotor(OUTPUT_B)
#right_motor = LargeMotor(OUTPUT_C)

#Initialize the two tacho motors
left_motor = Motor(OUTPUT_B)
right_motor = Motor(OUTPUT_C)

#TouchSensor - example code
"""
ts = TouchSensor(PORT) #Find the port later
Example code for TouchSensor from the devs
print("Press the touch sensor to change the LED color!")
while True:
    if ts.is_pressed:
        leds.set_color("LEFT", "GREEN")
        leds.set_color("RIGHT", "GREEN")
    else:
        leds.set_color("LEFT", "RED")
        leds.set_color("RIGHT", "RED")
"""

#UltraSonicSensor - example code
"""
ultrasonic_sensor = UltrasonicSensor(INPUT_1)
while True:
    debug_print(str(ultrasonic_sensor.distance_centimeters))
    time.sleep(0.1)
"""

#ColorSensor - example code
"""
cs = ColorSensor(INPUT_4)
while True:
    debug_print(cs.color)
    time.sleep(0.5)
"""

#Using the tank module to controle both of them at the same time
#tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
#tank_drive.on_for_rotations(SpeedPercent(75), SpeedPercent(75), 5)
#See function below

#Driving function, meaussered in rotations and a velocity, both motors
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
def drive_both_motors(speed, rotations):
    tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), rotations)

def drive_both_motors_forever(speed):
    MoveTank.on(SpeedPercent(speed), SpeedPercent(speed))

#Individual motors
#left_motor.on_for_rotations(SpeedPercent(75), 5)
#right_motor.on_for_rotations(SpeedPercent(75), 5) 
#steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C) #NOT FINISHED
def turn_left():
    left_motor.on_for_rotations(SpeedPercent(75), 1.5)

def turn_right():
    right_motor.on_for_rotations(SpeedPercent(75), 1.5)

def go_around():
    #Find good values
    turn_right()
    time.sleep(0.5)
    drive_both_motors(75, 3)
    time.sleep(0.5)
    turn_left()

#Simple "AI" car
#Main code
def car_code():
    while True:
        if ultrasonic_sensor.distance_centimeters > 15:
            drive_both_motors(75, 1)
        else:
            if random.randrange(1,4) == 1:
                go_around()
            elif random.randrange(1,4) == 2:
                turn_right(speed, rotations)
                turn_right(speed, rotations)
            elif random.randrange(1,4) == 3:
                time.sleep(5)