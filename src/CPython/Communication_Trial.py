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
        
    def run(self):
        self.uart_to_micro = self.serial.Serial(port='COM3', baudrate=115200, timeout=0.25)
        self.uart_to_micro.write(b'\x03')  # send Ctr+C
        self.time.sleep(0.5)  # sleep for half a second
        self.uart_to_micro.write(b'\x04')  # send Ctrl+D.
        self.uart_to_micro.write(self.text)  # send the packet over to the
        
if __name__ == '__main__':
    function = TextPrint()
    function.run()