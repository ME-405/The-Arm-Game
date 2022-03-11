'''!
@file    inputmain.py
@brief   This is a basic file in order to understand how the computer and micro-controller communicate 
@author  Nick De Simone, Jacob-Bograd, Horacio Albarran
@date	 March 10, 2022
'''

#from pyb import UART
#uart = UART(1, 115200)
#uart.init(115200)

while True:
    hello = input()
    print("Microcontroller " + hello)