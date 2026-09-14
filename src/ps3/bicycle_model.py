from math import *



if __name__ == '__main__':
    x = 0.118
    y = -0.54
    theta = 0.1
    alpha = 0.166
    d = 1.07
    L = 0.2

    radius = L / tan(alpha)
    beta = d / radius

    x_new = x - radius * sin(theta) + radius * sin(beta + theta)
    y_new = y + radius * cos(theta) - radius * cos(beta + theta)
    theta_new = (theta + beta) % (2 * pi)
    print(f'radius: {radius}')
    print(f'beta: {beta}')
    print(f'final pose: ({x_new}, {y_new}, {theta_new})')