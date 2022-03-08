import pygame
import serial
import time

# TODO MAKE THIS OUR OWN CODE THIS IS EXAMPLE CODE

# constants
XLIMIT = 4.65 * 2
YLIMIT = 4.65 * 2
ZLIMIT = 4.65 * 2
debug = False
ACK = True
# setup the UART
try:
    uart_to_micro = serial.Serial(port='COM5', baudrate=115200, timeout=0)
    # reset the Microcontroller
    uart_to_micro.write(b'\x03')  # send Ctr+C
    time.sleep(0.5)  # sleep for half a second
    uart_to_micro.write(b'\x04')  # send Ctrl+D
    uart_to_micro.reset_input_buffer()
    uart_to_micro.reset_output_buffer()
    time.sleep(5)
    debug = False
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
Yaxis = 4.6
Zaxis = 4.6  # start off as zero
to_print = "Nothing Yet"
previous_to_print = None
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
        # Format of the packet is [X, Y, Z, CLAW PITCH, CLAW CLOSE]
        # NOTE All joystick values are rounded to ONE decimal point due to joystick drift
        # R2 (Axis 5) is the claw
        claw_close = round((joystick.get_axis(5) + 1) * 90, 0)  # take the joystick input, make it from 0 - 2 then
        if claw_close > 45:
            claw_close = 45
        elif claw_close < 0:
            claw_close = 0

        # convert to angle
        claw_pitch = round((joystick.get_axis(4) + 1) * 90, 0)  # same as above
        if claw_pitch < 0:
            claw_pitch = 0
        elif claw_pitch > 90:
            claw_pitch = 90
        textPrint.tprint(screen, "Claw Pitch {}".format(claw_pitch))
        textPrint.tprint(screen, "Claw Angle {}".format(claw_close))
        buttons = joystick.get_numbuttons()
        textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.tprint(screen,
                             "Button {:>2} value: {}".format(i, button))
        textPrint.unindent()
        # Left Stick X (Axis 0) is X axis
        Xaxis = (joystick.get_button(14) * 0.1 + Xaxis)
        Xaxis = Xaxis - (joystick.get_button(13) * 0.1)

        #Xaxis = round(joystick.get_axis(0) + Xaxis, 1)

        # Left Stick Y (Axis 0) is Y axis
        Yaxis = (joystick.get_button(11) * 0.1) + Yaxis
        Yaxis = Yaxis - (joystick.get_button(12) * 0.1)
        #Yaxis = round((-1 * joystick.get_axis(1)) + Yaxis, 1)  # Negative 1 because joystick is backwards
        Xaxis = round(Xaxis, 3)
        Yaxis = round(Yaxis, 3)
        # L2 (Axis 4) is Z axis
        # 0 is ground 2 is max vertical
        Zaxis = round(((-1 * joystick.get_axis(3)) * 0.1) + Zaxis, 1)  # Negative 1 because joystick is backwards

        # check that the axis are not at their limit
        '''
        if Xaxis > XLIMIT:
            Xaxis = XLIMIT
        if Yaxis > YLIMIT:
            Yaxis = YLIMIT
        if Zaxis > ZLIMIT:
            Zaxis = ZLIMIT
        if Xaxis < -2.1:
            Xaxis = -2.1
        if Yaxis < -8:
            Yaxis = -8
            '''
        if Zaxis == 0:
            Zaxis = 0.000001
        if Xaxis == 0:  # hardcode to never be at 0 to avoid division by zero
            Xaxis = 0.000001
        if Yaxis == 0:
            Yaxis = 0.000001
        if Zaxis == 0:
            Zaxis = 0.000001

        textPrint.tprint(screen, "Coordinates: {},{},{}".format(Xaxis, Yaxis, Zaxis))

        if debug:
            to_print = "!!!DEBUG MODE, NOT CONNECTED TO MICROCONTROLLER!!!"
        elif ACK:  # The Microcontroller is ready for another packet
            packet_string = str(Xaxis) + "," + str(Yaxis) + "," + str(Zaxis) + "," + str(claw_pitch) + "," + str(
                claw_close) + '\r\n'
            # packet_string = str(4.6) + "," + str(4.6) + "," + str(4.6) + "," + str(135) + "," + str(45) + '\r\n'
            to_print = "Packet_string = " + packet_string
            uart_to_micro.write(packet_string.encode('utf-8'))  # send the packet over to the
            # print(f"PACKET SENT {packet_string.encode('utf-8')}")
            ACK = False  # Wait for the microcontroller to be ready for another packet
        else:  # check if the Microcontroller is ready for another packet
            temp_to_print = ""
            messages = uart_to_micro.readlines()
            for message in messages:
                if "ACK" in message.decode():
                    to_print = "Microcontroller is ready for another packet"
                    ACK = True
            if not ACK:
                temp_to_print = ""
                for message in messages:
                    temp_to_print += message.decode()
            if temp_to_print != "":
                to_print = temp_to_print
        #  if "ACK":
        #      to_print = "Microcontroller is ready for another packet"
        #      ACK = True  # it is ready for another packet
        # elif len(message) > 3:
        #    to_print = message
        # if previous_to_print != to_print:
        # print(to_print)
        previous_to_print = to_print
        textPrint.tprint(screen, to_print)
        textPrint.tprint(screen, f"Packet = {Xaxis}, {Yaxis}, {Zaxis}, {claw_pitch}, {claw_close}")
        try:
            textPrint.tprint(screen, f"PacketString = {packet_string}")
        except NameError:
            pass  # we are in debug mode

        textPrint.tprint(screen, f"MCU Ready = {ACK}")
        # END OF ME405 SECTION
        #########################################################################

    pygame.display.flip()  # update the display

    # Limit to 20 frames per second.
    clock.tick(20)

pygame.quit()  # exit everything
