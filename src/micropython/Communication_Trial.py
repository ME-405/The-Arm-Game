from pyb import UART

uart = UART(2)  # create a new UART connection with the specified channel and buadrate
uart.init(115200)

while True:
    #print("hello")
    if uart.any() != 0:
        print('hello whats popping')
        uart.read()
