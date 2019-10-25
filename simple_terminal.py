#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import ev3dev2.button

#Hacks
import subprocess, os, time, sys

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def run_command(command):
    commmand = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    STDOUT, STDERR = commmand.communicate()
    #STDOUT is the important one
    return STDOUT.decode('UTF-8') #Otherwise \n is weird

os.system('setfont Lat15-TerminusBold14')
# os.system('setfont Lat15-TerminusBold32x16')  # Try this larger font
# A full list of fonts can be found with `ls /usr/share/consolefonts`

debug_print(run_command("")) #To CODE output

#print(run_command("cd ..; cd ..; ls")) #To the EV3 screen
#time.sleep(15)  # display the text long enough for it to be seen - again EV3