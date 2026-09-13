from robot_pf import robot
import math


if __name__ == '__main__':
    my_robot = robot()

    my_robot.set_noise(5.0, 0.1, 5.0)
    my_robot.set(30., 50., math.pi / 2)
    print(my_robot)
    my_robot = my_robot.move(-1 * math.pi / 2, 15)
    print(my_robot.sense())

    my_robot = my_robot.move(-1 * math.pi / 2, 10)
    print(my_robot.sense())