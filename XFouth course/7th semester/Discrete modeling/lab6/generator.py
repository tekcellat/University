import numpy.random as nr
import numpy as np


class Generator(object):
    def __init__(self, random=None):
        if random is not None:
            self._random = random
        else:
            self._random = nr.RandomState()

    def next(self):
        raise NotImplementedError


class UniformGenerator(Generator):
    def __init__(self, m, d, random=None):
        super().__init__(random)
        self._a = m - d
        self._b = m + d
        if not 0 <= self._a <= self._b:
            raise ValueError('Параметры должны удовлетворять условию 0 <= a <= b')

    def next(self):
        return self._random.uniform(self._a, self._b)


class ConstGenerator(Generator):
    def __init__(self, m):
        super().__init__()
        if m < 0:
            raise ValueError('Параметр должен быть больше 0')
        self._m = m

    def next(self):
        return self._m


class ExponentialGenerator:
    def __init__(self, lmbd=0.09, random=None):
        super().__init__()
        if lmbd < 0:
            raise ValueError('Параметр должен быть больше 0')
        self._lambda = 1 / lmbd

    def next(self):
        return 1 - np.exp(-self._lambda * nr.exponential(self._lambda))