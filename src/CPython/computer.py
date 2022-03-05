import pygame
import serial
import time

# TODO MAKE THIS OUR OWN CODE THIS IS EXAMPLE CODE

# constants
XLIMIT = 10
YLIMIT = 10
ZLIMIT = 10
debug = False
ACK = False
# setup the UART
try:
    uart = serial.Serial(port='com3', baudrate=115273, timeout=1)
    # reset the Microcontroller
    uart.write(b'\x03')  # send Ctr+C
    time.sleep(0.5)  # sleep for half a second
    uart.write(b'\x04')  # send Ctrl+D
    time.sleep(0.5)
except serial.serialutil.SerialException:
    print("INVALID UART, ENTERING DEBUGGING MODE")
    debug = True

# TODO CLEAN UP BELOW

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("The-Arm-Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

# intinalize the starting variables
Xaxis = 0
Yaxis = 0
Zaxis = 0  # start off as zero

# -------- Main Program Loop -----------
while not done:
    #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get():  # User did something.
        if event.type == pygame.QUIT:  # If user clicked close.
            done = True  # Flag that we are done so we exit this loop.

    #
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()
    # Get count of joysticks.  # DEBUG
    joystick_count = pygame.joystick.get_count()  # DEBUG
    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))  # DEBUG
    textPrint.indent()  # DEBUG

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            # get_instance_id() is an SDL2 method
            jid = joystick.get_id()
        textPrint.tprint(screen, "Joystick {}".format(jid))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        try:
            guid = joystick.get_guid()
        except AttributeError:
            # get_guid() is an SDL2 method
            pass
        else:
            textPrint.tprint(screen, "GUID: {}".format(guid))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = round(joystick.get_axis(i), 1)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()

        ########################################################################
        # NOW WE START THE ME405 SECTION
        # Format of the packet is [X, Y, Z, CLAW]
        # NOTE All joystick values are rounded to ONE decimal point due to joystick drift
        # R2 (Axis 5) is the claw
        claw_close = round((joystick.get_axis(5) + 1) * 90, 0)  # take the joystick input, make it from 0 - 2 then
        # convert to angle
        claw_pitch = round((joystick.get_axis(4) + 1) * 90, 0)  # same as above
        textPrint.tprint(screen, "Claw Pitch {}".format(claw_pitch))
        textPrint.tprint(screen, "Claw Angle {}".format(claw_close))

        # Left Stick X (Axis 0) is X axis
        Xaxis = round(joystick.get_axis(0) + Xaxis, 1)

        # Left Stick Y (Axis 0) is Y axis
        Yaxis = round((-1 * joystick.get_axis(1)) + Yaxis, 1)  # Negative 1 because joystick is backwards

        # L2 (Axis 4) is Z axis
        # 0 is ground 2 is max vertical
        Zaxis = round((-1 * joystick.get_axis(3)) + Zaxis, 1)  # Negative 1 because joystick is backwards

        # check that the axis are not at their limit

        if Xaxis > XLIMIT:
            Xaxis = XLIMIT
        if Yaxis > YLIMIT:
            Yaxis = YLIMIT
        if Zaxis > ZLIMIT:
            Zaxis = ZLIMIT
        if Xaxis < -XLIMIT:
            Xaxis = -XLIMIT
        if Yaxis < -YLIMIT:
            Yaxis = YLIMIT
        if Zaxis < -ZLIMIT:
            Zaxis = -ZLIMIT
        if Xaxis == 0:  # hardcode to never be at 0 to avoid division by zero
            Xaxis = 0.0000000000001

        textPrint.tprint(screen, "Coordinates: {},{},{}".format(Xaxis, Yaxis, Zaxis))

        if debug:
            textPrint.tprint(screen, "!!!DEBUG MODE, NOT CONNECTED TO MICROCONTROLLER!!!")
        elif ACK:  # The Microcontroller is ready for another packet
            packet = [Xaxis, Yaxis, Zaxis, claw_pitch, claw_close]
            uart.write(packet)  # send the packet over to the
            ACK = False  # Wait for the microcontroller to be ready for another packet
        else:  # check if the Microcontroller is ready for another packet
            if uart.any():
                message = uart.read()
                if message == "ACK":
                    textPrint.tprint(screen, f"Microcontroller is ready for another packer")
                    ACK = True  # it is ready for another packet
        if not debug:
            if uart.any():
                message = uart.read()
                textPrint.tprint(screen, f"Microcontroller just said {message}")

        # END OF ME405 SECTION
        #########################################################################

    pygame.display.flip()  # update the display

    # Limit to 20 frames per second.
    clock.tick(20)

pygame.quit()  # exit everything
