# This is a servo test file

import pyb
from Motor import MotorDriver
from encoder import Encoder
from closedLoopControl import ClosedLoopController as clc


def main():
    p = pyb.Pin(pyb.Pin.board.PA5)  # , pyb.Pin.OUT, pyb.Pin.PULL_DOW)
    tim = pyb.Timer(2, freq=50)
    ch = tim.channel(1, pyb.Timer.PWM, pin=p)
    ch.pulse_width_percent(5)

    p2 = pyb.Pin(pyb.Pin.board.PA6)  # , pyb.Pin.OUT, pyb.Pin.PULL_DOW)
    tim2 = pyb.Timer(3, freq=50)
    ch2 = tim2.channel(1, pyb.Timer.PWM, pin=p2)
    ch2.pulse_width_percent(5)

    p3 = pyb.Pin(pyb.Pin.board.PA7)  # , pyb.Pin.OUT, pyb.Pin.PULL_DOW)
    # tim3 = pyb.Timer(3, freq=50)
    ch3 = tim2.channel(2, pyb.Timer.PWM, pin=p3)
    ch3.pulse_width_percent(5)

    p4 = pyb.Pin(pyb.Pin.board.PC7)  # , pyb.Pin.OUT, pyb.Pin.PULL_DOW)
    tim4 = pyb.Timer(8, freq=50)
    ch4 = tim4.channel(2, pyb.Timer.PWM, pin=p4)
    ch4.pulse_width_percent(5)

    # Instantiated object for the encoder as well as timer,
    #     encoderPin1 = pyb.Pin(pyb.Pin.board.PB6)
    #     encoderPin2 = pyb.Pin(pyb.Pin.board.PB7)
    #     EncTimer1 = 4
    #     EncoderDriver = Encoder(encoderPin1, encoderPin2, EncTimer1, 1, 2)
    #
    #     # Instantiated the objects for the motor
    #     motorEnable1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.IN, pyb.Pin.PULL_UP)
    #     motor1Pin1 = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    #     motor1Pin2 = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    #     motorTimer = pyb.Timer(5, freq=20000)
    #     Motor = MotorDriver(motorEnable1, motor1Pin1, motor1Pin2, motorTimer, 1, 2)
    #
    #     Motor.enable()
    #     cl = clc(EncoderDriver, Motor)
    #     cl.final_point = 188000
    #     another = cl.control_algorithm()
    while True:
        pwm = float(input("New PWM1"))
        #pwm = 1.5
        ch.pulse_width_percent(pwm)
        pwm2 = float(input("New PWM2"))
        ch2.pulse_width_percent(pwm2)
        #ch3.pulse_width_percent(pwm)
        #ch4.pulse_width_percent(pwm)


#          Motor.set_duty_cycle(-30)
# next(another)


if __name__ == '__main__':
    main()
