import matplotlib.pyplot as plt
import numpy as np


def plot_maker(masx, masy, xlabel, ylabel):
    plt.plot(masx, masy, color='r')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.legend((name1, name2))
    plt.grid(True)
    plt.show()

    def k(x):
        return a/(x - b)

    def alpha(x):
        return 3*x/(x - d)

    def P(Ax):
        return 2 * Ax / R

    def F(Ax):
        return (2 * T0 * Ax)/R

    def Xn_formula(x, h, flag):
        if flag == "+":
            res = 2 * k(x) * k(x + h) / (k(x) + k(x + h))
        if flag == "-":
            res = 2 * k(x) * k(x - h) / (k(x) + k(x - h))
        return res

    def An(x, h):
        res = 2 * k(x) * k(x - h) / (k(x) + k(x - h))
        return res/h

    def Bn(x, h, Ai, Ci):
        return Ai + Ci + P(x) * h

    def Cn(x, h):
        res = 2 * k(x) * k(x + h) / (k(x) + k(x + h))
        return res/h

    def Dn(x, h):
        return F(x) * h

    def get_K0(x0, h):
        pn_1_div_2 = (P(x0) + P(x0 + h)) / 2
        return Xn_formula(x0, h, "+") + h**2 * pn_1_div_2 / 8 + h**2 * P(x0)/4

    def get_M0(x0, h):
        pn_1_div_2 = (P(x0) + P(x0 + h)) / 2
        return -Xn_formula(x0, h, '+') + h**2 * pn_1_div_2 / 8

    def get_P0(x0, h):
        fn_1_div_2 = (F(x0) + F(x0 + h)) / 2
        return h * F0 + h**2 * (fn_1_div_2 + F(x0)) / 4

    def get_KN(x, h):
        res = 2 * k(x) * k(x - h) / (k(x) + k(x - h))
        return -P(x)*h/4 - (P(x-h) + P(x))*h/16 - alpha(x) - res/h

    def get_MN(x, h):
        res = 2 * k(x) * k(x - h) / (k(x) + k(x - h))
        return res/h - (P(x-h) + P(x))*h/16

    def get_PN(xn, h):
        return -alpha(xn) * T0 - h * (3*F(xn) + F(xn - h))/8

    def progon(A, B, C, D, K0, M0, P0, KN, MN, PN):
        xi = [0]
        eta = [0]
        xi.append(-M0/K0)
        eta.append(P0/K0)
        for i in range(1, len(A)):
            xi.append(C[i]/(B[i] - A[i]*xi[-1]))
            eta.append((D[i] + A[i] * eta[-1])/(B[i] - A[i]*xi[-2]))
        y = [(PN - MN*eta[-1]) / (KN + MN * xi[-1])]
        for i in range(len(A) - 2, -1, -1):
            y.reverse()
        return y

    k0 = 0.4
    kN = 0.1
    alpha0 = 0.05
    alphaN = 0.01
    l = 30
    T0 = 300
    R = 0.5
    F0 = 50
    h = 1e-3
    x0 = 0

    b = kN * l / (kN - k0)
    a = - k0 * b
    d = alphaN * l / (alphaN - alpha0)
    c = - alpha0 * d

    A = []
    B = []
    C = []
    D = []
    xmas = []

    for x in np.arange(x0, l + h, h):
        Ai, Ci, Di = An(x, h), Cn(x, h), Dn(x, h)
        Bi = Bn(x, h, Ai, Ci)

        A.append(Ai)
        B.append(Bi)
        C.append(Ci)
        D.append(Di)

    K0 = get_K0(x0, h)
    P0 = get_P0(x0, h)
    M0 = get_M0(x0, h)

    KN = get_KN(l, h)
    PN = get_PN(l, h)
    MN = get_MN(l, h)

    dots = progon(A, B, C, D, K0, M0, P0, KN, MN, PN)
    plot_maker(xmas[1:], dots[1:], 'Длина стержня, см', 'Температура, К')
