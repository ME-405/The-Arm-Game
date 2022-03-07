from pyb import USB_VCP
from nb_input import NB_Input
import utime

utime.sleep(1)

serial_stream = USB_VCP()
nb_in = NB_Input(serial_stream, echo=False)

while True:
    #print("test")
    #utime.sleep(.5)
    if nb_in.any() != 0:
        print("ACK")
        print("Input: ", nb_in.get())
