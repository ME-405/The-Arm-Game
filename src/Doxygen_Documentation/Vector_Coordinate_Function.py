'''!
@file    Vector_Coordinate_Function.py
@brief   It finds the angles for the elbow and arm for the ME-405 lab term project, such file can also be used in python in order to get the locations of the arm in 2D
@author  Nick De Simone, Jacob-Bograd, Horacio Albarran
@date	 March 10, 2022
'''

# Importing libraries
import math


# import matplotlib.pyplot as plt  # WILL NEED TO REMOVE THIS FOR


class ElArAngles:
    '''!
    @brief   Provides with the angles for the robot arm
    @details Using Inverse Kinematics (IK) the angle for the arm with respect 
                to the horizontal can be found as well as finding the angle required
                for the elbow in order reach the end-effector position described
                by the coordinates x and y
                Furthur, help/calculations were obtained from the following 
                MATLAB documentation :
                    https://www.mathworks.com/help/symbolic/derive-and-apply-inverse-kinematics-to-robot-arm.html
    '''

    def __init__(self):
        '''!
        @brief It will initialiaze the variables on the main file
        '''
        # Providing with the coordinates for the origin 
        self.origin = 0;

        # It creates a local variable for plt
        # self.plt = plt;

        # Creating the math variable
        self.math = math;

        # Given coordinates of desired point in space, end-effector location
        self.x = None
        self.y = None

        # Lengths of links
        self.leo = 4.65;  				# Length of elbow
        self.lBe = 4.65;  				# Length of arm

        # Creating arrays for data
        self.datax = [];
        self.datay = [];

    def set_angles(self, x, y):
		'''!
		@brief It provides with the x-and-y-coordinates as provided by the controller
		@param   x is the coordinate on the x-axis
        @param   y is the coordinate on the y-axis
		'''
        self.x = x						# x-coordinate provided by controller
        self.y = y						# y-coordinate provided by controller

    def plot(self, data_x, data_y):
        '''!
        @brief   It provides with a function to plot for the data provided. 
        @details The function needs inputs "datax" as day and "datay" as flu
                     state for the student in order to provide with a plot of 
                     the behavior of the student during a period of 50 days
					        @param   encoder set the parameter given for the chosen encoder
        @param   data_x is the array of x-values
		@param   data_y is the array of y-values
        '''

        # self.plt.plot(data_x, data_y, label='Robot Arm')
        # self.plt.ylabel('Vertical Distance')
        # self.plt.xlabel('Horizontal Distance')
        # self.plt.title ('Robotic Arm')
        # self.plt.grid()

    def run(self):
        '''!
        @brief It will run the file to calculate for the angles for the arm and elbow
        '''
        try:
            # if statements are to correct for singularity so that there is no
            # negative values placed on the x-y-coordinate
            if self.y > self.leo:
                # Equation to find the angle for the elbow
                self.tetha2_rad = 2 * self.math.atan(self.math.sqrt(
                    (-self.leo ** 2 + 2 * self.leo * self.lBe - self.lBe ** 2 + self.x ** 2 + self.y ** 2) * (
                                self.leo ** 2 + 2 * self.leo * self.lBe + self.lBe ** 2 - self.x ** 2 - self.y ** 2)) / (
                                                                 -self.leo ** 2 + 2 * self.leo * self.lBe - self.lBe ** 2 + self.x ** 2 + self.y ** 2))
                self.tetha2 = self.tetha2_rad * (180 / self.math.pi);  # Transforming the angles to degrees

                # Equations to find the angle for the arm
                self.phi1 = self.math.sqrt(
                    -self.leo ** 4 + 2 * (self.leo ** 2) * (self.lBe ** 2) + 2 * (self.leo ** 2) * (self.x ** 2) + 2 * (
                                self.leo ** 2) * (self.y ** 2) - self.lBe ** 4 + 2 * (self.lBe ** 2) * (self.x ** 2) + 2 * (
                                self.lBe ** 2) * (self.y ** 2) - self.x ** 4 - 2 * (self.x ** 2) * (
                                self.y ** 2) - self.y ** 4)
                self.tetha1_rad = 2 * self.math.atan((2 * self.leo * self.y - self.phi1) / (
                            self.leo ** 2 + 2 * self.leo * self.x - self.lBe ** 2 + self.x ** 2 + self.y ** 2))
                self.tetha1 = self.tetha1_rad * (180 / self.math.pi);  # Transforming the angles to degrees

            elif self.y <= self.leo:
                # Equation to find the angle for the elbow
                self.tetha2_rad = -2 * self.math.atan(self.math.sqrt(
                    (-self.leo ** 2 + 2 * self.leo * self.lBe - self.lBe ** 2 + self.x ** 2 + self.y ** 2) * (
                                self.leo ** 2 + 2 * self.leo * self.lBe + self.lBe ** 2 - self.x ** 2 - self.y ** 2)) / (
                                                                  -self.leo ** 2 + 2 * self.leo * self.lBe - self.lBe ** 2 + self.x ** 2 + self.y ** 2))
                self.tetha2 = self.tetha2_rad * (180 / self.math.pi);  # Transforming the angles to degrees

                # Equations to find the angle for the arm
                self.phi1 = self.math.sqrt(
                    -self.leo ** 4 + 2 * (self.leo ** 2) * (self.lBe ** 2) + 2 * (self.leo ** 2) * (self.x ** 2) + 2 * (
                                self.leo ** 2) * (self.y ** 2) - self.lBe ** 4 + 2 * (self.lBe ** 2) * (self.x ** 2) + 2 * (
                                self.lBe ** 2) * (self.y ** 2) - self.x ** 4 - 2 * (self.x ** 2) * (
                                self.y ** 2) - self.y ** 4)
                self.tetha1_rad = 2 * self.math.atan((2 * self.leo * self.y + self.phi1) / (
                            self.leo ** 2 + 2 * self.leo * self.x - self.lBe ** 2 + self.x ** 2 + self.y ** 2))
                self.tetha1 = self.tetha1_rad * (180 / self.math.pi)

                # Creating an array with the values for the angles for the elbow and arm
            # of the robotic arm
            self.angles = [self.tetha1_rad, self.tetha2_rad]

            # print(self.angles);                 # <--------------------------------- YIELD ANGLES IN HERE

            # ==============================================================================================================
            # Calculating locations for the joint of the elbow and the wrist
            # location as well as plotting the desired location to be ploted

            # Origin
            # self.plot(self.origin,self.origin, '*')
            # self.datax.append(self.origin)
            # self.datay.append(self.origin)

            # Elbow location
            self.elbowx = self.leo * self.math.cos(self.tetha1_rad);
            self.elbowy = self.leo * self.math.sin(self.tetha1_rad);
            # self.plot(self.elbowx,self.elbowy, '.')
            # self.datax.append(self.elbowx)
            # self.datay.append(self.elbowy)

            # print(self.elbowx,self.elbowy)

            # Arm location
            self.armx = self.elbowx + self.lBe * self.math.cos(self.tetha2_rad + self.tetha1_rad);
            self.army = self.elbowy + self.lBe * self.math.sin(self.tetha2_rad + self.tetha1_rad);
            # self.plot(self.armx,self.army,'.')
            # self.datax.append(self.armx)
            # self.datay.append(self.army)

            # print(self.armx,self.army)

            # Point of desired location at end of arm
            self.locx = self.x;
            self.locy = self.y;
            # self.plot(self.locx,self.locy,'x')

            # print(self.locx,self.locy)
        except ValueError:
            print("exception")

# ===============================================================================================================

# self.plot(self.datax,self.datay)            # Plotting mechanism
# self.plt.plot(self.locx, self.locy, '*', label='Desired Location')    # Plotting desired location, end-effector location
# self.plt.legend (loc='lower right')


## Dunder method to run the file automatically on the console pannel
if __name__ == '__main__':
    function = ElArAngles()
    function.run()
