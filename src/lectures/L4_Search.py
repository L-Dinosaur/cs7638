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

from Utilities import test

# SEARCH LESSON MODULES
print("SEARCH LESSON MODULES", end="")

# --------------------------------------------------------------------
# 9. FIRST SEARCH PROGRAM
print("\n9. FIRST SEARCH PROGRAM")
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
#
#  Comment out any print statements used for debugging.

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']

def search(grid, init, goal, cost):
    path = 'fail'
    open_list = [[0] + init]
    close_list = [init]
    def check_goal(s):
        if (s[1] == goal[0]) & (s[2] == goal[1]):
            return True
        return False

    def feasible(s):
        if (s[1] >= len(grid)) or (s[1] < 0):
            return False
        if (s[2] >= len(grid[0])) or (s[2] < 0):
            return False
        if grid[s[1]][s[2]] == 1:
            return False
        return True

    def closed(s):
        for c in close_list:
            if (s[1] == c[0]) and (s[2] == c[1]):
                return True
        return False

    while open_list:
        state = open_list.pop(0)
        for d in delta:
            new_state = [state[0] + cost, state[1] + d[0], state[2] + d[1]]
            if feasible(new_state) and (not closed(new_state)):
                open_list.append(new_state)
                close_list.append([new_state[1], new_state[2]])
                if check_goal(new_state):
                    return new_state
    return path


print(search(grid, init, goal, cost))

print("EXTRA TEST CASES (1):")
try:
    response = test.run_grader_1(search)
    print(response)
except Exception as err:
    print(str(err))

# --------------------------------------------------------------------
# 10. EXPANSION GRID
print("\n10. EXPANSION GRID")
# Modify the function search so that it returns
# a table of values called expand. This table
# will keep track of which step each node was
# expanded.
#
# Make sure that the initial cell in the grid
# you return has the value 0.
#
#  Comment out any print statements used for debugging.

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']

import copy
def search(grid, init, goal, cost):
    path = 'fail'
    open_list = [[0] + init]
    close_list = [init]
    expand = copy.deepcopy(grid)
    expand_num = 0
    for i in range(len(expand)):
        for j in range(len(expand[0])):
            if (i == init[0]) and (j == init[1]):
                expand[i][j] = expand_num
                expand_num += 1
            else:
                expand[i][j] = -1
    def check_goal(s):
        if (s[1] == goal[0]) & (s[2] == goal[1]):
            return True
        return False

    def feasible(s):
        if (s[1] >= len(grid)) or (s[1] < 0):
            return False
        if (s[2] >= len(grid[0])) or (s[2] < 0):
            return False
        if grid[s[1]][s[2]] == 1:
            return False
        return True

    def closed(s):
        for c in close_list:
            if (s[1] == c[0]) and (s[2] == c[1]):
                return True
        return False

    while open_list:
        state = open_list.pop(0)
        for d in delta:
            new_state = [state[0] + cost, state[1] + d[0], state[2] + d[1]]
            if feasible(new_state) and (not closed(new_state)):
                open_list.append(new_state)
                close_list.append([new_state[1], new_state[2]])
                expand[new_state[1]][new_state[2]] = expand_num
                expand_num += 1
                if check_goal(new_state):
                    return new_state, expand

    return path, expand


path, expand = search(grid, init, goal, cost)
print('Path:', path)
print('Expand:')
for i in range(len(expand)):
    print(expand[i])


print("EXTRA TEST CASES (2):")
try:
    response = test.run_grader_2(search)
    print(response)
except Exception as err:
    print(str(err))

# --------------------------------------------------------------------
# 11. PRINT PATH
print("\n11. PRINT PATH")
# Modify the the search function so that it returns
# a shortest path as follows:
#
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left,
# up, and down motions. Note that the 'v' should be
# lowercase. '*' should mark the goal cell.
#
# You may assume that all test cases for this function
# will have a path from init to goal.

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']

import math
def search(grid, init, goal, cost):
    # Copy and paste your solution code from the previous exercise (#10)
    path = 'fail'
    open_list = [[0] + init]
    close_list = [init]
    expand = copy.deepcopy(grid)
    expand_num = 0
    policy = copy.deepcopy(grid)
    for i in range(len(expand)):
        for j in range(len(expand[0])):
            if (i == init[0]) and (j == init[1]):
                expand[i][j] = expand_num
                expand_num += 1
            else:
                expand[i][j] = -1
            policy[i][j] = ' '
    def check_goal(s):
        if (s[1] == goal[0]) & (s[2] == goal[1]):
            return True
        return False

    def feasible(s):
        if (s[1] >= len(grid)) or (s[1] < 0):
            return False
        if (s[2] >= len(grid[0])) or (s[2] < 0):
            return False
        if grid[s[1]][s[2]] == 1:
            return False
        return True

    def closed(s):
        for c in close_list:
            if (s[1] == c[0]) and (s[2] == c[1]):
                return True
        return False

    while open_list:
        state = open_list.pop(0)
        for d in delta:
            new_state = [state[0] + cost, state[1] + d[0], state[2] + d[1]]
            if feasible(new_state) and (not closed(new_state)):
                open_list.append(new_state)
                close_list.append([new_state[1], new_state[2]])
                expand[new_state[1]][new_state[2]] = expand_num
                expand_num += 1
                if check_goal(new_state):
                    path = new_state
                    break

    def revert(i):
        if i == 0:
            return 2
        elif i == 1:
            return 3
        elif i == 2:
            return 0
        elif i == 3:
            return 1
        else:
            raise ValueError('out of bound')

    if path != 'fail':
        pos = copy.deepcopy(goal)
        policy[pos[0]][pos[1]] = '*'
        while pos != init:
            cost_xy = math.inf
            prev_x = 0
            prev_y = 0
            direction = ' '
            for i, d in enumerate(delta):
                x_temp = pos[0] + d[0]
                y_temp = pos[1] + d[1]
                if (x_temp >= 0) and (x_temp < len(grid)) and (y_temp >= 0) and (y_temp < len(grid[0])) and (expand[x_temp][y_temp] != -1):
                    if expand[x_temp][y_temp] < cost_xy:
                        cost_xy = expand[x_temp][y_temp]
                        prev_x = x_temp
                        prev_y = y_temp
                        direction = delta_name[revert(i)]
            pos = [prev_x, prev_y]
            policy[prev_x][prev_y] = direction

    return path, expand, policy


path, expand, policy = search(grid, init, goal, cost)
for i in range(len(policy)):
    print(policy[i])

# --------------------------------------------------------------------
# 13. IMPLEMENT A*
print("\n13. IMPLEMENT A*")
# Modify the the search function so that it becomes
# an A* search algorithm as defined in the previous
# lectures.
#
# Your function should return the expanded grid
# which shows, for each element, the count when
# it was expanded or -1 if the element was never expanded.
#
# If there is no path from init to goal,
# the function should return the string 'fail'

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
heuristic = [[9, 8, 7, 6, 5, 4],
             [8, 7, 6, 5, 4, 3],
             [7, 6, 5, 4, 3, 2],
             [6, 5, 4, 3, 2, 1],
             [5, 4, 3, 2, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def search(grid, init, goal, cost, heuristic):
    # Copy and paste your solution code from the previous exercise (#11)
    # TODO: CHANGE/UPDATE CODE
    path = None
    expand = []
    policy = []





    return path, expand, policy


path, expand, policy = search(grid, init, goal, cost, heuristic)
for i in range(len(expand)):
    print(expand[i])

# --------------------------------------------------------------------
# 18. VALUE PROGRAM
print("\n18. VALUE PROGRAM")
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal.
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def compute_value(grid, goal, cost):
    value = []
    # TODO: ADD CODE HERE
    # make sure your function returns a grid of values as
    # demonstrated in the previous video.
    return value


value = compute_value(grid, goal, cost)
for i in range(len(value)):
    print(value[i])

# --------------------------------------------------------------------
# 19. OPTIMUM POLICY
print("\n19. OPTIMUM POLICY")
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
#
# Unnavigable cells as well as cells from which
# the goal cannot be reached should have a string
# containing a single space (' '), as shown in the
# previous video. The goal cell should have '*'.

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def compute_value(grid, goal, cost):
    value = []
    policy = []
    # Copy and paste your solution code from the previous exercise (#18)
    # TODO: CHANGE/UPDATE CODE

    return value, policy


value, policy = compute_value(grid, goal, cost)
for i in range(len(policy)):
    print(policy[i])

# --------------------------------------------------------------------
# 20. LEFT TURN POLICY
print("\n20. LEFT TURN POLICY")
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's
# optimal path to the position specified in goal;
# the costs for each motion are as defined in cost.

# grid format:
#     0 = navigable space
#     1 = unnavigable space
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0]  # given in the form [row,col,direction]

goal = [2, 0]  # given in the form [row,col]

cost = [2, 1, 20]  # cost has 3 values, corresponding to making a right turn, no turn, and a left turn

# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a
# right turn.

forward = [[-1,  0],  # go up
            [0, -1],  # go left
            [1,  0],  # go down
            [0,  1]]  # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


def optimum_policy2D(grid,init,goal,cost):
    value = [[[999 for col in range(len(grid[0]))] for row in range(len(grid))],
             [[999 for col in range(len(grid[0]))] for row in range(len(grid))],
             [[999 for col in range(len(grid[0]))] for row in range(len(grid))],
             [[999 for col in range(len(grid[0]))] for row in range(len(grid))]]
    # TODO: ADD CODE HERE
    policy2D = []
    return policy2D


policy2D = optimum_policy2D(grid, init, goal, cost)
for i in range(len(policy2D)):
    print(policy2D[i])
