from robot_pf import  robot, eval
from resampling_wheel import ResamplingWheel


if __name__ == '__main__':


    # print(my_robot)
    T = 10
    N = 1000
    p = []
    my_robot = robot()

    for i in range(N):
        x = robot()
        x.set_noise(0.05, 0.05, 5.)
        p.append(x)

    for t in range(T):
        my_robot = my_robot.move(0.1, 5.)
        Z = my_robot.sense()
        # print(f'Ground truth measurement: {Z}')
        # print(f'Ground truth location: {my_robot}')
        print(f'Localization Goodness: {eval(my_robot, p)}')

        p2 = []
        for i in range(N):
            p2.append(p[i].move(0.1, 5.))
        p = p2

        w = []
        for i in range(N):
            w.append(p[i].measurement_prob(Z))

        resampler = ResamplingWheel(w, N)
        result = resampler.resample()

        for i in range(N):
            p2[i] = p[result[i]]
        p = p2

