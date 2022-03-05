# This is a class to handle the servos

import pyb
import math


class Servo:
    def __init__(self, pin, timer_number, channel_number):
        self.pin = pin  # save the pin number
        # setup the timer with the frequency from the datasheet
        self.timer = pyb.Timer(timer_number, freq=50)
        self.channel = self.timer.channel(channel_number, pyb.Timer.PWM, pin=self.pin)

    def SetAngleRadian(self, radian):
        degree = radian * (180 / math.pi)
        self.SetAngle(degree)

    def SetAngle(self, degree):
        pulse = degree * (2/3)  # update the conversion factor
        self.channel.pulse_width(pulse)  # set the pulse width
        pass