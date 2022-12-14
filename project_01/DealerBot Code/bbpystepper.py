"""
--------------------------------------------------------------------------
bbpystepper
--------------------------------------------------------------------------
License:   
Copyright 2022 Abinand Parthasarathy

Based on library from

Copyright 2013 Pete Bachant, adapted to interact with a hall effect sensor

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

bbpystepper is a Python module used to control a stepper motor via the 
BeagleBone
"""

from __future__ import division
import Adafruit_BBIO.GPIO as GPIO
import time
import math

import hall_effect_sensor as hall

def initialize_pins(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

def set_all_pins_low(pins):
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
        
def wavedrive(pins, pin_index):
    for i in range(len(pins)):
        if i == pin_index:
            GPIO.output(pins[i], GPIO.HIGH)
        else:
            GPIO.output(pins[i], GPIO.LOW)

def fullstep(pins, pin_index):
    """pin_index is the lead pin"""
    GPIO.output(pins[pin_index], GPIO.HIGH)
    GPIO.output(pins[(pin_index+3) % 4], GPIO.HIGH)
    GPIO.output(pins[(pin_index+1) % 4], GPIO.LOW)
    GPIO.output(pins[(pin_index+2) % 4], GPIO.LOW)


class Stepper(object):
    def __init__(self, steps_per_rev=2048.0,
                 pins=["P8_13", "P8_14", "P8_15", "P8_16"],
                 hall_effect_bus=1, hall_effect_address = 0x60):

        self.pins = pins
        
        initialize_pins(self.pins)
        set_all_pins_low(self.pins)
        
        self.angle = 0
        self.steps_per_rev = steps_per_rev
        
        # Initialize stepping mode
        self.drivemode = fullstep
        
        # Hall Effect Sensor
        self.sensor = hall.HallEffectSensor(hall_effect_bus = 1, hall_effect_address = 0x60)
        
    
    def rotate(self, degrees=360, rpm=15):
        """Rotates the stepper motor a specific number of degrees at a specified rpm """
        step = 0
        
        # Calculate time between steps in seconds
        wait_time = 60.0/(self.steps_per_rev*rpm)
        
        # Convert degrees to steps
        steps = math.fabs(degrees*self.steps_per_rev/360.0)
        self.direction = 1
        
        if degrees < 0:
            self.pins.reverse()
            self.direction = -1
        
        while step < steps:
            for pin_index in range(len(self.pins)):
                self.drivemode(self.pins, pin_index)
                time.sleep(wait_time)
                step += 1
                self.angle = (self.angle + self.direction/self.steps_per_rev \
                *360.0) % 360.0
        
        if degrees < 0:
            self.pins.reverse()
    	
        set_all_pins_low(self.pins)
        
    def zero_angle(self):
        self.angle = 0
        
        
    def go_to_initial_position(self):
        """ rotates stepper motor until initial position (determined by hall effect sensor) is reached """
        while(self.sensor.in_position() == 0):
            print("rotating motor")
            time.sleep(0.05)

def main():
    stepper = Stepper()
    stepper.rotate()
    

if __name__ == "__main__":
    stepper = Stepper()
    stepper.go_to_initial_position()