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

from Utilities.references import *
from Utilities.robot_slam import *
from rait import matrix

# SLAM LESSON MODULES
print("SLAM LESSON MODULES", end="")

# --------------------------------------------------------------------
# 7. SEGMENTED CTE
print("\n7. SEGMENTED CTE")
# Familiarize yourself with the code in references.py
# Most of it reproduces results that you have obtained at some
# point in this class. Once you understand the code,
# write a function, cte, in the run function that
# computes the crosstrack error for the case of a segmented path.
# You will need to include the equations shown in the video.


# grid format:
#   0 = navigable space
#   1 = occupied space

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 0]]

init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]

steering_noise = 0.1
distance_noise = 0.03
measurement_noise = 0.3

weight_data = 0.1
weight_smooth = 0.2
p_gain = 2.0
d_gain = 6.0


# run:  runs control program for the robot
def run(grid, goal, spath, params, printflag=False, speed=0.1, timeout=1000):
    myrobot = robot()
    myrobot.set(0., 0., 0.)
    myrobot.set_noise(steering_noise, distance_noise, measurement_noise)
    filter_ = particles(myrobot.x, myrobot.y, myrobot.orientation,
                        steering_noise, distance_noise, measurement_noise)

    cte = 0.0
    err = 0.0
    N = 0

    index = 0  # index into the path

    while not myrobot.check_goal(goal) and N < timeout:

        diff_cte = - cte

        # ----------------------------------------
        # compute the CTE
        # start with the present robot estimate
        estimate = filter_.get_position()

        # TODO: ADD CODE HERE

        # ----------------------------------------

        diff_cte += cte

        steer = - params[0] * cte - params[1] * diff_cte

        myrobot = myrobot.move(grid, steer, speed)
        filter_.move(grid, steer, speed)

        Z = myrobot.sense()
        filter_.sense(Z)

        if not myrobot.check_collision(grid):
            print('##### Collision ####')

        err += (cte ** 2)
        N += 1

        if printflag:
            print(myrobot, cte, index)

    return [myrobot.check_goal(goal), myrobot.num_collisions, myrobot.num_steps]


# this is our main routine
def main(grid, init, goal, steering_noise, distance_noise, measurement_noise,
         weight_data, weight_smooth, p_gain, d_gain):
    path = plan(grid, init, goal)
    path.astar()
    path.smooth(weight_data, weight_smooth)
    return run(grid, goal, path.spath, [p_gain, d_gain])


print(main(grid, init, goal, steering_noise, distance_noise, measurement_noise,
           weight_data, weight_smooth, p_gain, d_gain))

# --------------------------------------------------------------------
# 8. FUN WITH PARAMETERS
print("\n8. FUN WITH PARAMETERS")
# The point of this exercise is to find the optimal
# parameters! You can write a twiddle function or you
# can use any other method that you like!

# grid format:
#   0 = navigable space
#   1 = occupied space

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 0]]

init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]

steering_noise = 0.1
distance_noise = 0.03
measurement_noise = 0.3

#### ADJUST THESE PARAMETERS ######
weight_data = 0.1
weight_smooth = 0.2
p_gain = 2.0
d_gain = 6.0
###################################

# TODO: ADD CODE HERE

# --------------------------------------------------------------------
# 18. OMEGA AND XI
print("\n18. OMEGA AND XI")
# Write a function, doit, that takes as its input an
# initial robot position, move1, and move2. This
# function should compute the Omega and Xi matrices
# discussed in lecture and should RETURN the mu vector
# (which is the product of Omega.inverse() and Xi).


"""
For the following example, you would call doit(-3, 5, 3):
3 robot positions
  initially: -3
  moves by 5
  moves by 3
which should return a mu of:
[[-3.0],
 [2.0],
 [5.0]]
"""


def doit(initial_pos, move1, move2):
    mu = None
    # TODO: ADD CODE HERE
    return mu


doit(-3, 5, 3)

# --------------------------------------------------------------------
# 20. EXPAND
print("\n20. EXPAND")
# Modify your doit function to incorporate 3
# distance measurements to a landmark(Z0, Z1, Z2).
# You should use the provided expand function to
# allow your Omega and Xi matrices to accomodate
# the new information.
#
# Each landmark measurement should modify 4
# values in your Omega matrix and 2 in your
# Xi vector.
"""
For the following example, you would call doit(-3, 5, 3, 10, 5, 2):
3 robot positions
  initially: -3 (measure landmark to be 10 away)
  moves by 5 (measure landmark to be 5 away)
  moves by 3 (measure landmark to be 2 away)
which should return a mu of:
[[-3.0],
 [2.0],
 [5.0],
 [7.0]]
"""


def doit(initial_pos, move1, move2, Z0, Z1, Z2):
    mu = None
    # Copy and paste your solution code from the previous exercise (#18)
    # TODO: UPDATE CODE

    return mu


doit(-3, 5, 3, 10, 5, 2)

# --------------------------------------------------------------------
# 22. CONFIDENT MEASUREMENTS
print("\n22. CONFIDENT MEASUREMENTS")
# Modify the previous code to adjust for a highly
# confident last measurement. Do this by adding a
# factor of 5 into your Omega and Xi matrices
# as described in the video.

def doit(initial_pos, move1, move2, Z0, Z1, Z2):
    mu = None
    # Copy and paste your solution code from the previous exercise (#20)
    # TODO: UPDATE/MODIFY CODE

    return mu


mu = doit(-3, 5, 3, 10, 5, 1)

if mu != None:
    mu.show()

# --------------------------------------------------------------------
# 23. IMPLEMENTING SLAM
print("\n23. IMPLEMENTING SLAM")
# In this problem you will implement SLAM in a 2 dimensional
# world. Please define a function, slam, which takes five
# parameters as input and returns the vector mu. This vector
# should have x, y coordinates interlaced, so for example,
# if there were 2 poses and 2 landmarks, mu would look like:
#  mu =  matrix([[Px0],
#                [Py0],
#                [Px1],
#                [Py1],
#                [Lx0],
#                [Ly0],
#                [Lx1],
#                [Ly1]])
# data - This is the data that is generated with the included
#        make_data function. You can also use test_data to
#        make sure your function gives the correct result.
# N -    The number of time steps.
# num_landmarks - The number of landmarks.
# motion_noise - The noise associated with motion. The update
#                strength for motion should be 1.0 / motion_noise.
# measurement_noise - The noise associated with measurement.
#                     The update strength for measurement should be
#                     1.0 / measurement_noise.

"""
The order of actions is sense, then move.
"""


# slam - retains entire path and all landmarks
def slam(data, N, num_landmarks, motion_noise, measurement_noise):
    #
    # TODO: ADD CODE HERE
    #
    return mu  # Make sure you return mu for grading!

num_landmarks      = 5        # number of landmarks
N                  = 20       # time steps
world_size         = 100.0    # size of world
measurement_range  = 50.0     # range at which we can sense landmarks
motion_noise       = 2.0      # noise in robot motion
measurement_noise  = 2.0      # noise in the measurements
distance           = 20.0     # distance by which robot (intends to) move each iteratation

data = make_data(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)
result = slam(data, N, num_landmarks, motion_noise, measurement_noise)
if result != None:
    print_result(N, num_landmarks, result)
