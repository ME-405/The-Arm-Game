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
        self.serial = serial
        self.time = time
        self.uart = self.serial.Serial(port='COM5', baudrate=115273, timeout=0)

    #  self.uart.close()

    def run(self):
        # self.uart.open()
        self.uart.write(b'\x03')  # send Ctr+C
        self.time.sleep(0.5)  # sleep for half a second
        self.uart.write(b'\x04')  # send Ctrl+D.
        self.time.sleep(3)
        self.uart.reset_input_buffer()
        self.uart.reset_output_buffer()
        # self.uart.close()

        # and endless while loop that prompts the user for input then sends it over uart and then
        # reads the uart and prints it out.

        while True:
            # self.uart.open()
            self.text = input("What to send ")
            self.uart.write((self.text + '\r\n').encode('utf-8'))
            time.sleep(1)
            notRead = True
            messages = 0
            ACK = False
            while notRead:
                if self.uart.inWaiting() != 0:
                    # read = self.uart.readline().decode().strip()
                    # waste = self.uart.readline()
                    read = self.uart.readlines()
                    # print(read)
                    for line in read:
                        decoded = line.decode().strip()
                        print(decoded)
                        if "ACK" in decoded:
                            ACK = True
                    print("The microcontorller says", ACK)
                    notRead = False
        #            self.uart.close()

        self.uart.write(self.text)  # send the packet over to the


if __name__ == '__main__':
    function = TextPrint()
    function.run()
