######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

# Please note that the following methods listed below are incomplete:
# make_heuristic, astar, smooth,
# Use the lectures and videos for help on finishing them yourselves. Good luck!

from math import *
from copy import deepcopy
import random


class plan:
    # --------
    # init:
    #    creates an empty plan
    #

    def __init__(self, grid, init, goal, cost=1):
        self.cost = cost
        self.grid = grid
        self.init = init
        self.goal = goal
        self.make_heuristic()
        self.path = []
        self.spath = []

    # --------
    #
    # make heuristic function for a grid

    def make_heuristic(self):
        '''
        grid (2D list containing 0s and 1s): representing (un)navigable portions of the grid
        goal (list of ints of len 2): represents goal location as indices
        cost (int): represents the cost to move in any direction

        '''
        self.heuristic = [[0 for col in range(len(self.grid[0]))]
                          for row in range(len(self.grid))]

        raise NotImplementedError('Student code not implemented (comment out this line when done)')

        # TODO: Implement a manhattan dist for the heuristic

    # ------------------------------------------------
    #
    # A* for searching a path to the goal
    #
    #

    def astar(self):
        '''
        Note: Instead of path being a 2d grid as shown in lectures, please set self.path
        to a list of [x,y] locations in the order of the path from the start to the goal.

        There is no need to return values since 'self' is being updated
        (i.e. Use self.grid for grid, self.init for init, self.heuristic for
        heuristic,self.goal for goal, and self.cost for cost)

        elements in the open list are in the following format: [f, g, h, x, y]
        '''

        if self.heuristic == []:
            raise ValueError("Heuristic must be defined to run A*")

        # internal motion parameters
        delta = [[-1, 0],  # go up
                 [0, -1],  # go left
                 [1, 0],  # go down
                 [0, 1]]  # do right


        # TODO: Fill in this method using a modified solution code of
        #  exercise/lesson #13 in Search Module (do NOT return values)

        # ------------------------------------------------
        # Finish code for this method here!
        # ------------------------------------------------

        raise NotImplementedError('Student code not implemented (comment out this line when done)')




    # ------------------------------------------------
    #
    # this is the smoothing function
    #

    def smooth(self, weight_data=0.1, weight_smooth=0.1,
               tolerance=0.000001):

        if self.path == []:
            raise ValueError("Run A* first before smoothing path")

        # TODO: Fill in this method using a modified solution code of
        #  exercise/lesson #6 in PID Module (do NOT return values)
        # (i.e. Use self.path for path, and self.spath for newpath)
        # There is no need to return values since 'self' is being updated

        # The code is started for you below
        self.spath = deepcopy(self.path)  # spath is similar to newpath from lesson modules

        # ------------------------------------------------
        # Finish code for this method here!
        # ------------------------------------------------

        raise NotImplementedError('Student code not implemented (comment out this line when done)')



# ------------------------------------------------
#
# this is the robot class
#

class robot:

    # --------
    # init:
    #	creates robot and initializes location/orientation to 0, 0, 0
    #

    def __init__(self, length=0.5):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.measurement_noise = 0.0
        self.num_collisions = 0
        self.num_steps = 0

    # --------
    # set:
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)

    # --------
    # set_noise:
    #	sets the noise parameters
    #

    def set_noise(self, new_s_noise, new_d_noise, new_m_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)
        self.measurement_noise = float(new_m_noise)

    # --------
    # check:
    #    checks if the robot pose collides with an obstacle, or
    # is too far outside the plane

    def check_collision(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    dist = sqrt((self.x - float(i)) ** 2 +
                                (self.y - float(j)) ** 2)
                    if dist < 0.5:
                        self.num_collisions += 1
                        return False
        return True

    def check_goal(self, goal, threshold=1.0):
        dist = sqrt((float(goal[0]) - self.x) ** 2 + (float(goal[1]) - self.y) ** 2)
        return dist < threshold

    # --------
    # move:
    #    steering = front wheel steering angle, limited by max_steering_angle
    #    distance = total distance driven, most be non-negative

    def move(self, grid, steering, distance,
             tolerance=0.001, max_steering_angle=pi / 4.0):

        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        raise NotImplementedError('Student code not implemented (comment out this line when done)')
        # TODO: Fill in this method using a modified solution code of
        #  Problem Set 3 Question 6 (move function)
        # Finish code for this method here! Apply noise, then execute motion.


        # check for collision
        # res.check_collision(grid)

        return  # return the robot

    # --------
    # sense:
    #

    def sense(self):

        return [random.gauss(self.x, self.measurement_noise),
                random.gauss(self.y, self.measurement_noise)]

    # --------
    # measurement_prob
    #    computes the probability of a measurement
    #

    def measurement_prob(self, measurement):
        '''
        measurement (list of floats of len 2): represents (x,y) location of target measurement

        Using the Gaussian function below, calculate and return the relative likelihood of the
        measurement given the particle's location.
        This returned values will be used as the particle's weight.
        The weight should be based solely on the distance away from the measurement.
        '''

        # ---------------------------------------------------------------------------
        # TODO: invoke the Gaussian method below to calculate the relative likelihood.  Enter your code here.
        # ---------------------------------------------------------------------------


        raise NotImplementedError('Student code not implemented (comment out this line when done)')
        return weight


    def Gaussian(self, ):
        '''
        Finish this Gaussian method including the signature and implementation
        Use exercise/lesson #8 in the Kalman Filters modules for help
        '''

        # TODO: Implement a function that returns the relative likelihood of x given a Gaussian
        raise NotImplementedError('Student code not implemented (comment out this line when done)')

        return likelihood


    def __repr__(self):
        # return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)
        return '[%.5f, %.5f]' % (self.x, self.y)


# ------------------------------------------------
#
# this is the particle filter class
#

class particles:

    # --------
    # init:
    #	creates particle set with given initial position
    #

    def __init__(self, x, y, theta,
                 steering_noise, distance_noise, measurement_noise, N=100):

        self.N = N
        self.steering_noise = steering_noise
        self.distance_noise = distance_noise
        self.measurement_noise = measurement_noise

        self.data = []

        # TODO: Create a list (self.data) of N particles
        #  Be sure to set the position and noise for each
        raise NotImplementedError('Student code not implemented (comment out this line when done)')

    # --------
    #
    # extract position from a particle set
    #

    def get_position(self):
        x = 0.0
        y = 0.0
        orientation = 0.0

        for i in range(self.N):
            x += self.data[i].x
            y += self.data[i].y
            # orientation is tricky because it is cyclic. By normalizing
            # around the first particle we are somewhat more robust to
            # the 0=2pi problem
            orientation += (((self.data[i].orientation
                              - self.data[0].orientation + pi) % (2.0 * pi))
                            + self.data[0].orientation - pi)
        return [x / self.N, y / self.N, orientation / self.N]

    # --------
    #
    # motion of the particles
    #

    def move(self, grid, steer, speed):
        # TODO: Move all of the particles according to the input parameters
        #   Use exercise/lesson #14 in the Particle Filters module for help
        # Remember that self.data is similar to 'p' from the video modules

        raise NotImplementedError('Student code not implemented (comment out this line when done)')
        # self.data =

    # --------
    #
    # sensing and resampling
    #

    def sense(self, Z):
        raise NotImplementedError('Student code not implemented (comment out this line when done)')
        # TODO: Fill in this method using a modified solution code of
        #  exercise/lesson #21 in Particle Filter Module
        # Be sure to calculate the weights of the particles and then resample
        # Don't forget to update self.data (similar to p in videos)

        # self.data =


# If you encounter issues completing any of the methods above, 
# please reference the following SLAM module lecture videos:
# 6. Your Robot Car
# 7. Segmented CTE
