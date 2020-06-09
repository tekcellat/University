from math import *

class Data:
    def __init__(self):
        self.a_1 = 0.0134
        self.b_1 = 1.0
        self.c_1 = 4.35e-4
        self.m_1 = 1.0
        self.a_2 = 2.049
        self.b_2 = 0.563e-3
        self.c_2 = 0.528e5
        self.m_2 = 1.0
        self.alpha_0 = 0.05
        self.alpha_N = 0.01
        self.l = 10.0
        self.T_0 = 300.0
        self.R = 0.5
        self.F_0 = 50.0
        self.eps = 1e-4
        self.k_0 = 0.4
        self.k_N = 0.1
        self.a, self.b = self.get_a_b()
        self.c, self.d = self.get_c_d()

    def get_c_d(self):
        d = (self.alpha_N * self.l) / (self.alpha_N - self.alpha_0)
        c = self.alpha_0 * (-d)
        return c, d

    def F_t(self, t):
        return 10 + 20 * sin(t)

    def get_a_b(self):
        b = (self.k_N * self.l) / (self.k_N - self.k_0)
        a = self.k_0 * (-b)
        return a, b

    def k_x(self, x):
        return self.a / (x - self.b)

    #def X_n_and_half(self, x_n, x_n_and_1):
    #    return 2.0 * self.k_x(x_n) * self.k_x(x_n_and_1) / (self.k_x(x_n) + self.k_x(x_n_and_1))

    # метод трапеций
    def X_n_and_half(self, T_n, T_n_and_1):
        return 2.0 * self.k_T(T_n) * self.k_T(T_n_and_1) / (self.k_T(T_n) + self.k_T(T_n_and_1))

    def alpha_x(self, x):
        return self.c / (x - self.d)

    def f_x(self, x):
        return 2 * self.T_0 * self.alpha_x(x) / self.R

    def p_x(self, x):
        return 2 * self.alpha_x(x) / self.R

    def k_T(self, T):
        return self.a_1 * (self.b_1 + self.c_1 * pow(T, self.m_1))

    def c_T(self, T):
        return self.a_2 + self.b_2 * pow(T, self.m_2) - self.c_2 / (T * T)