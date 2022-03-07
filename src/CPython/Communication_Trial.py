# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 14:24:36 2022

@author: horac
"""

import serial
import time

class TextPrint(object):

    def __init__(self):
        self.text = 1
        self. serial = serial
        self.time = time
        self.uart = self.serial.Serial(port='COM5', baudrate=115200, timeout=0.25)

    def run(self):
        self.uart.write(b'\x03')  # send Ctr+C
        self.time.sleep(0.5)  # sleep for half a second
        self.uart.write(b'\x04')  # send Ctrl+D.
        self.time.sleep(3)
        self.uart.reset_input_buffer()
        self.uart.reset_output_buffer()

        while True:
            self.text = input("What to send ")
            self.uart.write(self.text.encode('ascii'))
            notRead = True
            messages = 0
            while notRead:
                if self.uart.inWaiting() != 0:
                    read = self.uart.readlines()
                    print(read)
                    notRead = False


        self.uart.write(self.text)  # send the packet over to the

if __name__ == '__main__':
    function = TextPrint()
    function.run()