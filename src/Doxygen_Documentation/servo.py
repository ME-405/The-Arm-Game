'''!
@file    servo.py
@brief   File used to handle the signal to the servos
@author  Nick De Simone, Jacob-Bograd, Horacio Albarran
@date	 March 10, 2022
'''
# Importing classes
import pyb
import math


class Servo:
	'''!
    @brief   Provides with the signal for the servos
    '''

    def __init__(self, pin, timer_number, channel_number):
		'''!
		@brief 		Initializing the function
		@param   	pin provides with the required pin for the servo signal
        @param   	timer_number provides with the required timer 
		@param      channel_number provides with the corresponding channel number for the signal
		'''
        self.pin = pin  # save the pin number
        # setup the timer with the frequency from the data-sheet
        self.timer = pyb.Timer(timer_number, freq=50)
        self.channel = self.timer.channel(channel_number, pyb.Timer.PWM, pin=self.pin)

    def SetAngleRadian(self, radian):
		'''!
		@brief 		This function transforms degrees to radians
		@param   	radian is the angle provided in units of radians
		'''
        degree = radian * (180 / math.pi)
        self.SetAngle(degree)

    def SetAngle(self, degree):
		'''!
		@brief 		This function sets the corresponding angle for the servo and transforms it to a signal for the corresponding servo
		@param   	degree is the corresponding angle to which the servo desires to be set  
		'''
        pulse = int(degree / 18) + 2  		     	# update the conversion factor, a conversion needed to be set since the servos only reacted
													# to numerical input from 2-12 in order to get a range from 0-180 degrees
        self.channel.pulse_width_percent(pulse) 	# set the pulse width
        #print(pulse)
