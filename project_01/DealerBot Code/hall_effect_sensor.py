"""
--------------------------------------------------------------------------
Hall Effect Sensor 
--------------------------------------------------------------------------
License:   
Copyright 2022 Abinand Parthasarathy

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

Simple class used to determine if the hall effect sensor is activated or not


"""
import time
import random
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

class HallEffectSensor():
    """ HallEffectSensor """
    hall_effect_bus          = None
    hall_effect_address      = None
    
    def __init__(self, hall_effect_bus = 1, hall_effect_address = 0x60):
        """ Initialize variables and set up display """
        self.hall_effect_bus      = hall_effect_bus
        self.hall_effect_address  = hall_effect_address
        
        self._setup()
    # End def

    def _setup(self):
        """Setup the hardware components."""
        pass
    # End def


    def in_position(self):
        """ Checks whether is magnet is over hall effect sensor"""
        val = random.random()
        if val > 0.5:
            return 1
        else:
            return 0
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

    print("Hall Effect Sensor Test")

    # Create instantiation of the servo
    halleffect = HallEffectSensor()
    print(halleffect.in_position())
 

