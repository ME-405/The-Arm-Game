"""!
@file    closedLoopControl.py
@details Close loop control runs and manages data interaction produced by the hardware 
@author  Nick De Simone, Jacob-Bograd, Horacio Albarran
@date    March 10, 2022
"""


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
        self.kp = .05
        self.ki = 0
        self.gain = 0  					# the gain will be updated in a function
        self.encoder = encoder
        self.motor = motor
        self.send_error = 0
        self.send_actuation = 0
        self.error_sum = 0

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
        self.encoder.set_position(0)  														# zero out the encoder value
        # NOTE This clc will run endlessly for the robotic arm mission
        while True:
            self.encoder.update()  															# update the encoder value
            error = self.final_point - self.encoder.current_pos 	 						# get the error
            self.error_sum += error*(10/1E6)
            voltage = 3.3  																	# Voltage used for the micro-controller
            actuation = (error * self.kp) / voltage + (self.ki*self.error_sum) / voltage  	# get the actuation
            if actuation >= 90:  															# It does not let it go too fast
                self.motor.set_duty_cycle(90)
                self.send_actuation = 90
          #  elif 20 >= actuation > 10:  # It does not let it stall
          #      self.motor.set_duty_cycle(20)
          #  elif -20 <= actuation < -10:  # It does not let it stall
          #      self.motor.set_duty_cycle(-20)
            elif actuation <= -90:  														# It does not let it go too fast
                self.motor.set_duty_cycle(-90)
                self.send_actuation = -90
            elif -30 <= actuation <= 30:  													# we are there
                self.motor.set_duty_cycle(0)  												# stop the motor until we get another position
                self.send_actuation = 0
            else:  																			# keep going
                self.motor.set_duty_cycle(actuation)
                self.send_actuation = actuation
            # print(f"final Point {self.final_point}, current point {self.encoder.current_pos}, actuation {actuation}")
            # DEBUG print statement below
            self.send_error = error

            # print(f"MCU DEBUG: error: {error}, actuation: {actuation}, current pos {self.encoder.current_pos}")

            yield 0  																		# let the next task do its job
