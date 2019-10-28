#!/usr/bin/env python3
from ev3dev2.motor import Motor, LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.wheel import EV3Tire
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
#ultrasonic_sensor = UltrasonicSensor(INPUT_1)
#ultrasonic_sensor.mode = 'US-DIST-CM'
"""
while True:
    debug_print(str(ultrasonic_sensor.distance_centimeters))
    time.sleep(0.1)
"""

#ColorSensor - example code
cs = ColorSensor(INPUT_3)
"""
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
    tank_drive.on(speed, speed)

#Individual motors
#left_motor.on_for_rotations(SpeedPercent(75), 5)
#right_motor.on_for_rotations(SpeedPercent(75), 5) 
#steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C) #NOT FINISHED
def turn_right():
    left_motor.on_for_rotations(SpeedPercent(25), 1.5)

def turn_left():
    right_motor.on_for_rotations(SpeedPercent(25), 1.5)

def little_right():
    left_motor.on_for_rotations(25, 0.1)
    right_motor.on_for_rotations(25, -0.1)

def little_left():
    right_motor.on_for_rotations(25, 0.1)
    left_motor.on_for_rotations(25, -0.1)

def go_around():
    #Find good values
    turn_right()
    time.sleep(0.5)
    drive_both_motors(50, 1)
    time.sleep(0.5)
    turn_left()

#Car code
def car_code():
    while True:
        while ultrasonic_sensor.distance_centimeters > 20:
            drive_both_motors_forever(25)
        #For stopping the motors
        left_motor.stop()
        right_motor.stop()
        time.sleep(0.2)
        #See above function
        go_around()

#Follow-the-line code
#Simplify the functions check_1 and check_2
n = 1
def check_1():
    n = 2
    for i in range(2):
            little_left()
            if cs.color == 1:
                follow_the_line()
            for i in range(2): 
                little_right()
            for i in range(2):
                little_right()
                if cs.color == 1:
                    follow_the_line()
    

def check_2():
    n = 1
    for i in range(2):
        little_right()
        if cs.color == 1:
            follow_the_line()
        for i in range(2): 
            little_left()
        for i in range(2):
            little_left()
            if cs.color == 1:
                follow_the_line()

def follow_the_line():
    if cs.color ==1 :
        drive_both_motors(25, 0.1)
        follow_the_line()
    else:
        if n == 1:
            check_1()
        else:
            check_2()

#Uncomment the following code for activating follow_the_line
#while True:
#    follow_the_line()

#Fighter code
#Notes on fighter robot:
#   Arms for "lifting" other robots
#   Something to support the robot if someones tries to lift it (i.e. some LEGO that prevents it from falling)
#   Depending on the number of avaible sensors the on_circle function can be improved
def check_for_opponent(num):
    #1 means that the robot is facing the opponent, 0 means that the robot is NOT facing the opponent
    if ultrasonic_sensor.distance_centimeters < num:
        return 1
    else:
        return 0

def get_dist():
    return ultrasonic_sensor.distance_centimeters

tire = EV3Tire

#Init arm
#arm = Motor(OUTPUT_A) #Find actual port
def lift_arm(k):
    #Init some more motors (regular one, as the LargeMotor will be used for driving)
    arm.on_for_rotations(100, k)

def ram_opponent(dist):
    rotations = dist / tire.circumference_cm #Read more on documentation (might now work with circumference_cm)
    drive_both_motors(100, rotations + 1) #Added value to push opponents out of the circle (find better value)
    lift_arm(5)
    drive_both_motors(100, 3) #Find better value

def on_circle():
    #For black
    if cs.color == 1:
        return True

def main_fighter():
    while True:
        if check_for_opponent(num) == 1:
            dist = get_dist()
            ram_opponent(dist)
        elif check_for_opponent(num) == 0:
            while True:
                if check_for_opponent(num) == 1:
                    break
                little_right()
