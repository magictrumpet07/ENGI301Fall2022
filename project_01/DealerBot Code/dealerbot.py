"""
--------------------------------------------------------------------------
DealerBot
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

Use the HT16K33 Display, potentiometer, push button, dc motor, stepper motor, light sensor, and hall effect sensor to control a minature robot that deals cards

Operation:
- User selects a game (War or Poker) by rotating the potentiometer to change the hex display output and pressing the button to select a game

- If War is chosen, two equal piles are dealt and the display resets to the beginning

- If Poker is chosen, the user can select the number of players again via the potentiometer and the button
    - When the user is ready for the cards in the flop, turn, or river to be dealt, they can press the push button to begin dealing
    - The device resets to the beginning after the river card is dealt
    
The ht16k33 class is provided by Erik Welsh for ENGI 301
The bbpystepper class is adapted from Pete Bachant

"""
import time

import Adafruit_BBIO.GPIO as GPIO

import ht16k33 as HT16K33
import dc_motor as DC_MOTOR
import bbpystepper as STEPPER_MOTOR
import hall_effect_sensor as hall
import Adafruit_BBIO.ADC as ADC



# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

poker_players = [(0, 1023, 2, "2"),
                 (1024, 2047, 3, "3"),
                 (2048, 3071, 4, "4"),
                 (3072, 4095, 5, "5")]

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class DealerBot():
    """ DealerBot """
    games               = None
    display             = None
    analog_in           = None
    button              = None
    dcmotor             = None
    steppermotor        = None
    
    def __init__(self, i2c_bus=1, i2c_address=0x70, dc_motor_pin = "P2_17",
        stepper_motor_pin = ["P2_4", "P2_6", "P2_8", "P2_10"], button="P2_2", analog_in="P1_19"):
        """ Initialize variables and set up display """
        self.button       = button
        self.display      = HT16K33.HT16K33(i2c_bus, i2c_address)
        self.analog_in    = analog_in
        self.dcmotor      = DC_MOTOR.DCMotor(dc_motor = dc_motor_pin, light_bus = 1, light_address = 0x29)
        self.steppermotor = STEPPER_MOTOR.Stepper(pins = stepper_motor_pin, hall_effect_bus = 1, hall_effect_address = 0x60)

        self.games        = [(0, 2047, self.start_poker, "po"),
                             (2048, 4095, self.war, "UUar")]

        self._setup()

    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""
        
        print("SETUP")
        # Initialize Display

        print("Initialize Display")
        
        # Check Light Sensor
        print("Check Light Sensor")
        
        # Calibrate Hall Effect
        print("Calibrate Hall Effect")
        
        # Initialize Analog Input
        print("Initialize analog input")
        #ADC.setup()

    # End def
    
    
    def deal_around(self, players = 1):
        """Deal a card to each player in the game:
               - rotate stepper motor depending on number of players
               - Call dcmotor.deal
        """

        for i in players:
            self.steppermotor.rotate(degrees = 180/(players + 1))
            
                # Call deal a card          
            self.dcmotor.deal()
        self.steppermotor.go_to_initial_position()

    # End def    

    def burn_a_card(self):
        """Burn a card from the top of a deck at the initial position:
               - Check hall effect sensor
               - Call deal_a_card
        """
        print("BURN A CARD")
        
        # Check hall effect
        #Checking Hall Effect Sensor- if under hall effect, deal. If not, rotate till hall effect
        self.steppermotor.go_to_initial_position()
        
        # Call deal a card
        self.dcmotor.deal()

    # End def

    def poker_flop(self):
        """ Burns a card and deals three cards for the flop:
            - burns a card to horizontal position
            - deals three cards evenly spaced
            - returns to original position
        """
        self.burn_a_card()
        for i in range(3):
            self.steppermotor.rotate(degrees = 30)
            self.dc_motor.deal()
        self.steppermotor.go_to_initial_position()
    # End def
    
    def poker_turn(self):
        """ Burns a card and deals one card to the fourth position:
            - burns a card to horizontal position
            - deals one card to fourth position
            - returns to original position
        """
        self.burn_a_card()
        self.steppermotor.rotate(degrees = 120)
        self.dc_motor.deal()
        self.steppermotor.go_to_initial_position()
    # End def
    
    def poker_river(self):
        """ Burns a card and deals one card to the fourth position:
            - burns a card to horizontal position
            - deals one card to fifth position
            - returns to original position
        """
        self.burn_a_card()
        self.steppermotor.rotate(degrees = 150)
        self.dc_motor.deal()
        self.steppermotor.go_to_initial_position()
    # End def
    
    def war(self):
        """ Deals every card in the deck into two even piles """
        
        self.steppermotor.go_to_initial_position()
        self.steppermotor.rotate(degrees = 60)
        
        for i in range(26):
            self.dcmotor.deal()
            self.steppermotor.rotate(degrees = 60)
            self.dcmotor.deal()
            self.steppermotor.rotate(degrees = -60)
        
        self.steppermotor.go_to_initial_position()
    
    # End def
        
    def poker_game(self, players = 4):
        """ Runs full game of poker, waiting for user input to move to the flop, turn, and river rounds """
        
        self.deal_around(players) 
        
        self.display.update("flop")
        while(self.button == 1):
            time.sleep(0.1)
        while(self.button == 0):
            time.sleep(0.1)
            self.poker_flop()
            
        self.display.update("turn")
        while(self.button == 1):
            time.sleep(0.1)
        while(self.button == 0):
            time.sleep(0.1)
            self.poker_turn()
            
        self.display.update("ri")
        while(self.button == 1):
            time.sleep(0.1)
        while(self.button == 0):
            time.sleep(0.1)
            self.poker_river()
    # End def
    
    def start_poker(self):
        """Asks the user to select the number of players and calls poker_game  """
        num_players = self.choose_val(poker_players)
        self.poker_game(num_players)
    # End def
    
    
    def check_pot(self):
        """Updates the value of the potentiometer to the HEX display based on user assignments from input"""
        ret_val = None
        pot_val = self.ADC.read_raw(self.analog_in)
        
        for game in self.games:
            if (pot_value >= game[0]) and (pot_value <= game[1]):
                self.display.update(game[3])
                ret_value = game[2]
        return ret_val
        
    # End def   
    
    def choose_val(self, values):
        """Allows a value displayed by the HEX display to be chosen via a button push"""
        ret_val = None
        
        while(self.button == 1):
            ret_val = self.check_pot(values)
            time.sleep(0.1)
            
        while(self.button == 0):
            time.sleep(0.1)

        return ret_val
        
    # End def        
    
    
    def run(self):
        """Execute the main program."""
        
        self.display.set_game()
        
        while(True):
            self.display.update("ga")
            
            game = self.choose_val(self.games)
            game()
            
    

    def cleanup(self):
        """Cleanup the hardware components."""
        # self.steppermotor.go_to_initial_position()
        print("Clean up hardware components")

        
    # End def

# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
if __name__ == '__main__':

    print("Program Start")
    
    dealerbot = DealerBot()

    try:
        # Run the lock
        dealerbot.run()

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        dealerbot.cleanup()

    print("Program Complete")
