"""
--------------------------------------------------------------------------
DC Motor Test
--------------------------------------------------------------------------
License:   
Copyright 2021-2022 Erik Welsh

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

Test SG90 Servo

"""

import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

import light_sensor as light

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------



# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class DCMotor():
    """ Servo """
    dc_motor      = None
    
    def __init__(self, dc_motor="EDIT", light_sensor_pin = ""):
        """ Initialize variables and set up display """
        self.dc_motor      = dc_motor
        
        self._setup()
        
        self.lightsensor = light.LightSensor(light_sensor=light_sensor_pin)
    
    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""
        pass

    # End def


    def deal(self):
        """Spin DC Motor to deal a card"""
        # Set servo
        lighttest = self.lightsensor.in_position()
        print(lighttest)
        if lighttest == 1:
            self._deal_a_card()
    # End def

    def _deal_a_card(self):
        """Action of spinning motor"""
        print("DC Motor ON")
        time.sleep(1)
        print("DC Motor OFF")

    # End def


    def cleanup(self):
        """Cleanup the hardware components."""
        
        pass
    # End def

# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("DC Motor Test")

    # Create instantiation of the motor
    dc_motor = DCMotor()
    dc_motor.deal()



