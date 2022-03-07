from pyb import USB_VCP
from nb_input import NB_Input

serial_stream = USB_VCP()
nb_in = NB_Input(serial_stream, echo=True)

while True:
    if nb_in.any():
        print("\r\nInput: ", nb_in.get())
