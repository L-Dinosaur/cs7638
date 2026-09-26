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

from Utilities.robot_pf import *

# PARTICLE FILTER LESSON MODULES
print("PARTICLE FILTER LESSON MODULES", end="")

# --------------------------------------------------------------------
# 8. USING A ROBOT CLASS
print("\n8. USING A ROBOT CLASS")
# For this lesson, (and the following lesson #9),
# please familiarize yourself with the robot class.

myrobot = robot()
myrobot.set(10, 10, 0)
print(myrobot)
myrobot = myrobot.move(pi/2, 10)
print(myrobot)
print(myrobot.sense())

# --------------------------------------------------------------------
# 10. MOVING ROBOT
print("\n10. MOVING ROBOT")
# Make a robot called myrobot that starts at
# coordinates 30, 50 heading north (pi/2).
# Have your robot turn clockwise by pi/2, move
# 15 m, and sense. Then have it turn clockwise
# by pi/2 again, move 10 m, and sense again.
# Your program should print out the result of
# your two sense measurements.

myrobot = robot()
# TODO: ADD CODE HERE

# --------------------------------------------------------------------
# 11. ADD NOISE
print("\n11. ADD NOISE")
# Now add noise to your robot as follows:
# forward_noise = 5.0, turn_noise = 0.1, sense_noise = 5.0.
#
# Once again, your robot starts at 30, 50,
# heading north (pi/2), then turns clockwise
# by pi/2, moves 15 meters, senses,
# then turns clockwise by pi/2 again, moves
# 10 m, then senses again.

myrobot = robot()
# TODO: ADD CODE HERE


# --------------------------------------------------------------------
# 13. CREATING PARTICLES
print("\n13. CREATING PARTICLES")
# Now we want to create particles,
# p[i] = robot(). In this assignment, write
# code that will assign 1000 such particles
# to a list.
# Your program should print out the length
# of your list (don't cheat by making an
# arbitrary list of 1000 elements!)

N = 1000
p = []
# TODO: ADD CODE HERE
print(len(p))

# --------------------------------------------------------------------
# 14. ROBOT PARTICLES
print("\n14. ROBOT PARTICLES")
# Now we want to simulate robot
# motion with our particles.
# Each particle should turn by 0.1
# and then move by 5.

# TODO: ADD CODE HERE

# --------------------------------------------------------------------
# 15. IMPORTANCE WEIGHT
print("\n15. IMPORTANCE WEIGHTS")
# Now we want to give weight to our
# particles. This program will print a
# list of 1000 particle weights.

myrobot = robot()
myrobot = myrobot.move(0.1, 5.0)
Z = myrobot.sense()

N = 1000
p = []

# Copy and paste your solution code from the previous exercises (#13 and #14)
# Note that there will need to be a small modification for setting noise to the
# previous code as stated in the video

w = []
# TODO: ADD CODE HERE
print(w)

# --------------------------------------------------------------------
# 20. NEW PARTICLE
print("\n20. NEW PARTICLE")
# In this exercise, try to write a program that
# will resample particles according to their weights.
# Particles with higher weights should be sampled
# more frequently (in proportion to their weight).

p3 = []
# TODO: ADD CODE HERE
p = p3

# --------------------------------------------------------------------
# 21. RESAMPLING WHEEL
print("\n21. RESAMPLING WHEEL")
# In this exercise, you should implement the
# resampler shown in the previous video.
'''
The pseudocode in the video should be like this (instead of an if-else block):

while w[index] < beta:
    beta = beta - w[index]
    index = (index + 1) % N

select p[index]
'''
myrobot = robot()
myrobot = myrobot.move(0.1, 5.0)
Z = myrobot.sense()

N = 1000
p = []

# Copy and paste your solution code from the previous exercise (#15)

p3 = []
# TODO: ADD CODE HERE
p = p3

# --------------------------------------------------------------------
# 23. ORIENTATION 2
print("\n23. ORIENTATION 2")
# In this exercise, write a program that will
# run your previous code twice.

N = 1000
myrobot = robot()
p = []

# Copy and paste your code from the previous exercise (#21)
# TODO: CHANGE/UPDATE CODE HERE

print(p)

# --------------------------------------------------------------------
# 24. ERROR
print("\n24. ERROR")
# In this exercise, write a program that will
# print out the quality of your solution
# using the eval function. (Should print T times!)

T = 10
N = 1000
myrobot = robot()
p = []

# Copy and paste your code from the previous exercise (#23)
# TODO: CHANGE/UPDATE CODE HERE
