# The motor test
import pyb
encoderPin1 = pyb.Pin(pyb.Pin.board.PC6)
encoderPin2 = pyb.Pin(pyb.Pin.board.PC7)
EncTimer1 = 8
EncoderDriver = Encoder(encoderPin1, encoderPin2, EncTimer1, 1, 2)

# Instantiated the objects for the motor
motorEnable1 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.IN, pyb.Pin.PULL_UP)
motor1Pin1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
motor1Pin2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
motorTimer = pyb.Timer(3, freq=20000)
Motor = MotorDriver(motorEnable1, motor1Pin1, motor1Pin2, motorTimer, 1, 2)

if __name__ == "__main__":


    
