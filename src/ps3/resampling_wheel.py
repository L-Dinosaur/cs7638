import numpy as np


class ResamplingWheel:
    def __init__(self, weights, N):
        self.w = weights
        self.wmax = np.max(weights)
        self.b = 0
        self.index = np.random.randint(0, N-1)
        self.result = []
        self.N = N

    def resample(self):
        for i in range(self.N):
            self.b = self.b + np.random.uniform(0, 2 * self.wmax) * 2
            while self.w[self.index] < self.b:
                self.b = self.b - self.w[self.index]
                self.index = (self.index + 1) % len(self.w)
            self.result.append(self.index)
        return self.result