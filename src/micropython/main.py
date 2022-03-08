'''!
@file main.py
@details This is the main file for the Micropython side of this project. It contains the FSM that controls the whole system.
'''

#  Importing libraries and classes
from pyb import USB_VCP
from nb_input import NB_Input
from servo import Servo
from Motor import MotorDriver
from encoder import Encoder
from closedLoopControl import ClosedLoopController as ClosedLoop
from pyb import UART
from Vector_Coordinate_Function import ElArAngles
import pyb
import gc
import cotask
import task_share
import math

INPUTINTERVAL = 10

DEFAULTANGLE = 60  # the default angle


# Instantiated the objects for the servos


def main():
    '''!
    @breif This is the main function that the MCU runs  whenever it is restarted
    '''
    # start by creating a share and queue
    arm = RoboticArm()  # make a new robotic arm

    # I am not sure if the share and queue are needed
    share = task_share.Share('h', thread_protect=False, name="Share")
    queue = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                             name="Queue")
    per_val = 5
    read_task = cotask.Task(arm.read_uart, name='read', priority=1, period=per_val, profile=False, trace=False)
    calculate_task = cotask.Task(arm.calculate_parameters, name='calculate', priority=1, period=per_val, profile=False,
                                 trace=False)
    update_task = cotask.Task(arm.update_parameters, name='update', priority=1, period=per_val, profile=False,
                              trace=False)
    clc_task = cotask.Task(arm.clc.control_algorithm, name='clc', priority=1, period=per_val, profile=False,
                           trace=False)
    # append all the tasks to the task list
    read = arm.read_uart()
    calculate = arm.calculate_parameters()
    update = arm.update_parameters()
    clc = arm.clc.control_algorithm()
    # cotask.task_list.append(read_task)
    # cotask.task_list.append(calculate_task)
    # cotask.task_list.append(update_task)
    # cotask.task_list.append(clc_task)

    gc.collect()
    # run the garbage collector

    # run the scheduler with round-robin since everything is the same\
    print("hello Computer")
    while True:
        next(read)
        # print("calculating")
        next(calculate)
        # print("Updating")
        next(update)
        # print("clc")
        #print(f"MCU DEBUG: error: {arm.clc.send_error}, actuation: {arm.clc.send_actuation}, current pos {arm.clc.encoder.current_pos}, final pos {arm.clc.final_point}")
       # for i in range(1, 10):
        next(clc)
        # cotask.task_list.pri_sched()  # this will never end, I think this is fine

    print("Look All Done")


class RoboticArm:
    def __init__(self, uart_channel=2, baudrate=115200):
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

        # Instantiated object for the encoder as well as timer,
        encoderPin1 = pyb.Pin(pyb.Pin.board.PB6)
        encoderPin2 = pyb.Pin(pyb.Pin.board.PB7)
        EncTimer1 = 4
        EncoderDriver = Encoder(encoderPin1, encoderPin2, EncTimer1, 1, 2)

        # Instantiated the objects for the motor
        motorEnable1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.IN, pyb.Pin.PULL_UP)
        motor1Pin1 = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
        motor1Pin2 = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
        motorTimer = pyb.Timer(5, freq=20000)
        Motor = MotorDriver(motorEnable1, motor1Pin1, motor1Pin2, motorTimer, 1, 2)

        # Conditions for UART  # TODO REMVOE THIS SECTION
       # self.uart_channel = uart_channel
       # self.baudrate = baudrate

        # Conditionals for the USB coms
        self.serial_stream = USB_VCP()
        self.nb_in = NB_Input(self.serial_stream, echo=False)

        # now setup all of the class variables

        # TODO remvoe THE UART
       # self.uart = UART(self.uart_channel,
          #              self.baudrate)  # create a new UART connection with the specified channel and buadrate
       # self.uart.init(115200)

        self.clc = ClosedLoop(EncoderDriver, Motor)  # make a new closed loop controller
        # self.command = [1, 0.1, 0.1, 100, 60]  #DEBUG
        self.command = None  # set the command to nothing

        # make the 4 servo objects, the pins are hard-coded
        # The setup for the pins might not be correct
        self.servo0 = Servo(pyb.Pin(pyb.Pin.board.PA5), 2, 1)  # The lower arm servo
        self.servo1 = Servo(pyb.Pin(pyb.Pin.board.PA6), 3, 1)  # The middle arm servo
        self.servo2 = Servo(pyb.Pin(pyb.Pin.board.PA7), 3, 2)  # The upper arm servo
        self.servo3 = Servo(pyb.Pin(pyb.Pin.board.PC7), 8, 2)  # The claw servo
        self.angles = [DEFAULTANGLE, DEFAULTANGLE, DEFAULTANGLE, DEFAULTANGLE]  # set all of the angles to default
        self.endpoint = DEFAULTANGLE  # Set the default endpoint
        self.new_values = False  # we do not have any new values to read
        # self.mail = True # DEBUG
        self.mail = False  # we do not have any mail from the computer
        self.VCF = ElArAngles()  # make the Vector Coordinate Function
        # TODO FIND THE CONVERSION FACTOR
        self.conversion_factor = 319  # The conversion factor from angle to encoder ticks

    # TODO ADD DOXY
    def read_uart(self):
        while True:
            if self.nb_in.any():
            #if True:
                # if self.uart.any():  # check if there is something in the pipeline
                # TODO MAKE IT BE ABLE TO HANDLE BAD COMMANDS
                command_string = self.nb_in.get().split(',')  # read in the command and split on ,
                # command_string = self.uart.read().decode('ascii').strip().split(
                #    ',')  # read the entire UART buss and split on ,
                # print(command_string)
                # print(command_string)
                self.command = [float(coordinate) for coordinate in command_string]  # convert the string list to float
                #print(f"Thank You")  # tell the computer you received the packet and it can send another one. TODO CHECK IF
                # NECESSARY
                print("ACK")  # we acknowledge
                self.mail = True  # we have some mail to sort through
            else:
               # print("No Mail")
                self.mail = False  # we have no new mail
            yield 0  # let another task have its turn in the spotlight

    # TODO ADD DOXY
    def calculate_parameters(self):
        # The format is X,Y,Z,CLAW PITCH, CLAW CLOSE
        while True:
            if self.mail:  # only calculate parameters if there is something that we need to do
                #  Get the base angle
                #  Ange = arctan(y/x)
                #  TODO CHECK ARCTAN CAN GET ALL ANGLES
                radians = math.atan2(self.command[1], self.command[0])  # get the angle in radians
                # TODO CHECK THAT THIS FORMULA IS CORRECT
                self.endpoint = radians * self.conversion_factor * 180 / math.pi  # convert the angle to encoder ticks
                #radius = math.sqrt(self.command[0]**2 + self.command[1]**2)
                self.VCF.set_angles(self.command[1], self.command[2])  # update the VCF with the new angles
                self.VCF.run()  # Have the VCF calculate the new angles

                # Get the angles for the 4 servos
                self.angles[0] = self.VCF.tetha1
                self.angles[1] = 180 - (self.VCF.tetha2 + 90)  # The servo is backwards
                # print(self.angles[1])  # DEBUG
                # The claw close and pitch are given as angles

                # TODO CHECK IF THESE SERVOS ARE INVERTED
                self.angles[2] = 180 - self.command[3]  # get the claw pitch value
                self.angles[3] = self.command[4]  # get the claw close value
                self.new_values = True
            yield 0  # send it back for another task to take over

    def update_parameters(self):
        while True:
            if self.new_values:
                # update the servo angles
                self.servo0.SetAngle(self.angles[0])
                self.servo1.SetAngle(self.angles[1])
                self.servo2.SetAngle(self.angles[2])
                self.servo3.SetAngle(self.angles[3])
                # update the base endpoint
                #print("New Endpoint = " + str(self.endpoint))
                self.clc.final_point = self.endpoint
                # print(f"angle0 {self.angles[0]} angle1 {self.angles[1]} angle2 {self.angles[2]} angle3 {self.angles[3]}")
            else:
                manual_breathing = 1  # you are now manually breathing
            yield 0  # let another function have its turn

    # this is just a simple pass-through to run the clc update
    def clc_passthrough(self):
        self.clc.control_algorithm()

    def zero_encoder(self):  # TODO CHECK IS THIS IS NESSARY
        '''!
        @brief This resets the encoder value in the clc to 0, for use in case of a failure and without a hardware reset
        '''
        self.clc.encoder.zero()


# Dunder method to run the function when the name of the file is main,
if __name__ == '__main__':
    main()
