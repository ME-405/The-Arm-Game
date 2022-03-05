"""!
@file    closedLoopControl.py
@details Close loop control runs and manages data interaction produced by the hardware 
@author  Nick De Simone, Jacob-Bograd, Horacio Albarran
@date    February 07, 2022
"""
'''
# I DONT THINK ANY OF THESE ARE NEEDED
# Importing the required classes and libraries
from Motor import MotorDriver
from encoder import Encoder
from pyb import Pin
from pyb import UART
import pyb
import time
import utime

'''


class ClosedLoopController:
    def __init__(self, encoder, motor):
        '''!
        @brief   closedLoopController manages the data provided by the encoder as well as running calculations
        @details This files manages the data provided by the encoder, it also manages the
                     setting values for the proper functioning of the motor, and any other
                     required calculations for the motor to work properly
        @param   encoder set the parameter given for the chosen encoder
        @param   motor provides with the chosen motor
        '''
        # TODO Document these class members
        # Setting some parameters
        self.final_point = 0
        self.kp = .5
        self.gain = 0  # the gain will be updated in a function
        self.encoder = encoder
        self.motor = motor

    def zero_encoder(self):
        '''!
        @details This is a simple function to zero out the encoder value
        '''
        self.encoder.zero()

    def control_algorithm(self):
        '''!
        @details It manages the value for kp as well as setting different
                    parameters for the duty cycle of the motor based on the
                    actuation value; which is dependent of the difference
                    encoder positions as well as the value of kp
        '''
        self.encoder.set_position(0)  # zero out the encoder value
        # NOTE This clc will run endlessly for the robotic arm mission
        while True:
            self.encoder.update()  # update the encoder value
            error = self.final_point - self.encoder.current_pos  # get the error
            voltage = 3.3  # Voltage used for the micro-controller
            actuation = (error * self.kp) / voltage  # get the actuation
            if actuation >= 90:  # dont let it go too fast
                self.motor.set_duty_cycle(90)
            elif 20 >= actuation > 5:  # dont let it stall
                self.motor.set_duty_cycle(20)
            elif -20 <= actuation < 5:  # dont let it stall
                self.motor.set_duty_cycle(-20)
            elif actuation <= 90:  # dont let it go too fast
                self.motor.set_duty_cycle(-90)
            elif -5 <= actuation <= 5:  # we are there
                self.motor.set_duty_cycle(0)  # stop the motor until we get another position
            else:  # keep going
                self.motor.set_duty_cycle(actuation)
            #print(f"final Point {self.final_point}, current point {self.encoder.current_pos}, accucation {actuation}")
            yield 0  # let the next task do its job
