'''!
@file controller.py
@details This is the file that contains all of the information for how to handle the dualsense (PS5) controller.

@author Jacob Bograd, Nick De Simone, Horacio Albarran
@date Feburary 21, 2022
'''

# TODO MOVE THIS TO A WORKING FRAMEWORK


from pydualsense import *
import time

def demo():
    '''!
    @breif This is a test demo to show off the libraries capabilities, a lot is taken from the official pydualsense github
    '''
    ps5 = pydualsense()
    ps5.init()

    print("Trigger Effect demo started")

    ps5.setLeftMotor(225)
    ps5.setRightMotor(100)
    ps5.triggerL.setmode(TriggerModes.Rigid)
    ps5.triggerL.setForce(1, 255)

    ps5.triggerR.setMode(TriggerModes.Pulse_A)
    ps5.triggerR.setForce(0, 200)
    ps5.TriggerR.setForce(1, 255)
    ps5.triggerR.setForce(2, 175)

    time.sleep(3)


    ps5.close()

if __name__ == '__main__':
    demo()


