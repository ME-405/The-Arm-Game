'''!
@file mainpage.py

@mainpage


@section sec_intro Introduction
Welcome to the lab repository for The-Arm-Game for ME 405. In this online repository website, it can be found 
all of the necessary files in order to perform the lab project assigned during the Winter 2022 quarter for the 
class of ME 405 at the California Polytechnic State University (Cal Poly) located at San Luis Obispo, Ca. 
lectured by Professor John R. Ridgely.

@section sec_Software_Design Software Design
The link for the Software Design code program is located at @ref page_Analysis_src

@section sec_Design_Analysis Software Design Analysis
For the analysis perform please refer to the following @ref page_Analysis




@page page_Analysis The Arm Game Analysis Page

@section page_Analysis_Introduction Introduction
Our goal is to create a robotic arm that a user can control using a game controller. The Controller will communicate
to the host computer over a library from GitHub. The Host controller will then interoperate the controller inputs 
and send them to the Nucleo. The Nucleo will read the inputs and update the respective motor PWM values. The Nucleo 
will then send the encoder values back to the computer. All of the calculations will be handled on the computer side
the Nucleo will only be setting the PWM values for the respective motors.

@section page_FSM The Arm Game Finite State Machine
The following Finite State diagrams gives a visual representation of the functioning of the code implemented for The Arm Game
** ADD FSM **

@section page_State_Diagram The Arm Game State Diagram
The following image provides with the require task for The Arm Game to function
** ADD FSM **

@section page_Analysis_src The Arm Game Source Code Access
You can find the source for The Arm Game sequence code in the following link:
** ADD LINK **


'''