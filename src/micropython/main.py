'''!
@file main.py
@details This is the main file for the micproython side of this project. It contains the FSM that controlls the whole system.
'''

#  Importing libraries and classes
import utime
from Motor import MotorDriver
from encoder import Encoder
from closedLoopControl import ClosedLoopController as closed_loop
from pyb import Pin
from pyb import Servo
from pyb import UART
import pyb
import gc
import cotask
import task_share



# Instantiated object for the encoder as well as timer,
encoderPin1 = pyb.Pin(pyb.Pin.board.PC6)
encoderPin2 = pyb.Pin(pyb.Pin.board.PC7)
EncTimer1 = 8
EncoderDriver = Encoder(encoderPin1, encoderPin2, EncTimer1, 1, 2)

# Instantiated the objects for the motor
motorEnable1 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.IN, pyb.Pin.PULL_UP)
motor1Pin1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
motor1Pin2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
motorTimer = pyb.Timer(3, freq=20000)
Motor = MotorDriver(motorEnable1, motor1Pin1, motor1Pin2, motorTimer, 1, 2)
input_interval = 10


# Instantiated the objects for the servos


# TODO SETUP THE CLASSES IN MAIN
def main():
    '''!
    @breif This is the main function that the MCU runs  whenever it is restarted
    '''
    pass


class robotic_arm:
    def __init__(self, uart_channel=1, baudrate=9600):
        '''!
        @brief TODO
        @details TODO
        @param uart_channel     This is the uart channel that we will be using for communication
        @param baudrate         This is the baudreate that we will be using for communication
        TODO update the doxygen from @param
        @param self.uart        This is the uart channel that we will be using for communication with the host machine
        @param self.clc         This is the close loop controller for the base
        @param self.command     This is the raw command taken from the host computer, it will be processed into angles and positions at a later date
        @param self.angles      This is a list that contains all of the angles for the servos to go to
        @param self.endpoint    This is the updated encoder endpoint for the base
        @param self.new_values  This is a boolean to determine if we need to update the parameters
        @param self.mail        This is a boolean to determine if we have new mail from the computer
        '''
        self.uart = UART(uart_channel, baudrate)  # create a new uart connection with the sepcified channel and buadrate
        self.clc = closed_loop(input_interval, EncoderDriver, Motor)  # make a new closed loop contorller
        self.command = None  # set the command to nothing
        # make the 4 servo objects, the pins are hardcoded
        # The setup for the pins might not be correct
        self.servo0 = pyb.Servo(pyb.Pin(pyb.Pin.board.PA5))  # The lower arm servo
        self.servo1 = pyb.Servo(pyb.Pin(pyb.Pin.board.PA6))  # The middle arm servo
        self.servo2 = pyb.Servo(pyb.Pin(pyb.Pin.board.PA7))  # The upper arm servo
        self.servo3 = pyb.Servo(pyb.Pin(pyb.Pin.board.PB6))  # The claw servo
        self.angles = [None, None, None, None]
        self.endpoint = None
        self.new_values = False  # we do not have any new values to read
        self.mail = False  # we do not have any mail from the computer

    def read_uart(self):
        if self.uart.any():  # check if there is something in the pipeline
            self.command = self.uart.read().split(",")  # read the entire uart buss and split on ,
            print('ACK')  # tell the computer you received the packet and it can send another one. TODO CHECK IF
            # NECESSARY
            self.mail = True  # we have some mail to sort through
        else:
            self.mail = False  # we have no new mail

    def calculate_parameters(self):
        # The format is X,Y,Z,CLAW

        # TODO take the points and make them parameters
        if self.mail:
            #  TODO do math to find the angles
            self.angle[3] = self.command[3]  # this is hardcoded to be like this
            pass
        pass

    def update_parameters(self):
        # TODO UPADTE THE PARAMETERS ONCE WE FIND THEM OUT.
        if self.new_values:
            # update the servo angles
            try:
                self.servo0.angle(self.angles[0])
                self.servo1.angle(self.angles[1])
                self.servo2.angle(self.angles[2])
                self.servo3.angle(self.angles[3])
                # update the base endpoint
                self.clc.update_setpoint(self.endpoint)
            except Exception:  # TODO FIND the exact exception to catch
                print("INVALID ANGLE DETECTED")  # tell the computer something went wrong
                # move on with your life

        else:
            pass  # nothing needs to be done

    def zero_encoder(self):  # TODO CHECK IS THIS IS NESSARY
        '''!
        @brief This resets the encoder value in the clc to 0, for use in case of a failure and without a hardware reset
        '''
        self.clc.encoder.zero()


if __name__ == '__main__':
    main()
