import numpy as np


from math import log, exp

To = 12000
Tw = 2000
m = 5

#First part
def solveIntegralNT(a, b, p):

    sum = .0
    N = 30
    step = (b - a) / (1.0 * N)

    for i in range(1, N):
        sum += NT(a + i * step, p)

    sum += (NT(a, p) + NT(b, p)) / 2
    sum *= step

    return sum


def Fp_funct(p):
    const_part = 7243.0 * (0.5 / 300.0)
    res = const_part - 2.0 * solveIntegralNT(0.0, 1.0, p)
    return res


def calculeateP(eps):
    p1 = 3.0
    p2 = 28.0

    p = (p1 + p2) / 2
    while abs((p2 - p1) / p) >= eps:
        p = (p1 + p2) / 2

        if Fp_funct(p)*Fp_funct(p1) < 0:
            p2 = p
        else:
            p1 = p
    return p


def TZ(z):
    zm = 1
    for i in range(1, m+1):
        zm *= z
    return To + (Tw - To)*zm


def NT(z, p):
    res = 1.0
    Tz = TZ(z)
    if Tz != 0:
        res = 7243.0 * (p / Tz) * z
    return res


p = calculeateP(1e-4)
print(p)
print("\n")



