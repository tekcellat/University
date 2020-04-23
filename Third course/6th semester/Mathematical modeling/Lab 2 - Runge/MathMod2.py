import numpy
import matplotlib.pyplot as plt
from decimal import Decimal
from scipy import integrate
from scipy.interpolate import InterpolatedUnivariateSpline
# одномерная кусочно-линейная интерполяция функции, которая задана точками (xp, fp).

# Table1
masI = [0.5,    1,    5,   10,   50,  200,   400,   800,  1200]
masT0 = [6400, 6790, 7150, 7270, 8010, 9185, 10010, 11140, 12010]
masm = [0.4, 0.55,  1.7,    3,   11,   32,    40,    41,    39]

# Table2
masT = [4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000]
masSigm = [0.031, 0.27, 2.05, 6.06, 12.0,
           19.9,  29.6,  41.1,  54.1,  67.7,  81.5]

# x - t время
# y - I ток
# z - Uc напряжение
# f - dI/dt
# phi - dU/dt


def interpolate(x, masX, masY):
    order = 1
    s = InterpolatedUnivariateSpline(masX, masY, k=order)
    return float(s(x))


def T(z):
    return (Tw - T0) * z**m + T0


def sigma(T):
    return interpolate(T, masT, masSigm)


def Rp(I):
    global m
    global T0
    m = interpolate(I, masI, masm)
    T0 = interpolate(I, masI, masT0)

    def func(z): return sigma(T(z)) * z
    integral = integrate.quad(func, 0, 1)
    Rp = le/(2 * numpy.pi * R**2 * integral[0])

    return Rp


def f(xn, yn, zn):
    return -((Rk + m_Rp_global) * yn - zn)/Lk


def phi(xn, yn, zn):
    return -yn/Ck


def second_order(xn, yn, zn, hn, m_Rp):
    global m_Rp_global

    m_Rp_global = m_Rp

    alpha = 0.5
    yn_1 = yn + hn * ((1 - alpha) * f(xn, yn, zn) + alpha
                      * f(xn + hn/(2*alpha),
                          yn + hn/(2*alpha) * f(xn, yn, zn),
                          zn + hn/(2*alpha) * phi(xn, yn, zn)))

    zn_1 = zn + hn * ((1 - alpha) * phi(xn, yn, zn) + alpha
                      * phi(xn + hn/(2*alpha),
                            yn + hn/(2*alpha) * f(xn, yn, zn),
                            zn + hn/(2*alpha) * phi(xn, yn, zn)))

    return yn_1, zn_1


def fourth_order(xn, yn, zn, hn, m_Rp):
    global m_Rp_global
    m_Rp_global = m_Rp

    k1 = hn * f(xn, yn, zn)
    q1 = hn * phi(xn, yn, zn)

    k2 = hn * f(xn + hn/2, yn + k1/2, zn + q1/2)
    q2 = hn * phi(xn + hn/2, yn + k1/2, zn + q1/2)

    k3 = hn * f(xn + hn/2, yn + k2/2, zn + q2/2)
    q3 = hn * phi(xn + hn/2, yn + k2/2, zn + q2/2)

    k4 = hn * f(xn + hn, yn + k3, zn + q3)
    q4 = hn * phi(xn + hn, yn + k3, zn + q3)

    yn_1 = yn + (k1 + 2*k2 + 2*k3 + k4)/6
    zn_1 = zn + (q1 + 2*q2 + 2*q3 + q4)/6

    return yn_1, zn_1


def do_plot(pltMasT, mas1, mas2, xlabel, ylabel, name1, name2):
    plt.plot(pltMasT, mas1)
    plt.plot(pltMasT, mas2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend((name1, name2))
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    R = 0.35
    Tw = 2000.0
    Ck = 268e-6
    Lk = 187e-6
    Rk = 0.25  # от 0.5 до 200
    Uc0 = 1400.0
    I0 = 0.5  # от 0.5 до 3
    le = 12.0

    I4 = I0
    Uc4 = Uc0
    I2 = I0
    Uc2 = Uc0

    T0 = 0.0
    m = 0.0

    pltMasTzero = []
    pltMasT = []
    pltMasI4 = []
    pltMasU4 = []
    pltMasRp4 = []
    pltMasI2 = []
    pltMasU2 = []
    pltMasRp2 = []

    h = 1e-5
    for t in numpy.arange(0, 0.0006, h):
        try:
            m_Rp4 = Rp(I4)
            m_Rp2 = Rp(I2)

            if t > h:
                pltMasT.append(t)
                pltMasTzero.append(T0)
                pltMasI4.append(I4)
                pltMasU4.append(Uc4)
                pltMasRp4.append(m_Rp4)
                pltMasI2.append(I2)
                pltMasU2.append(Uc2)
                pltMasRp2.append(m_Rp2)

            I4, Uc4 = fourth_order(t, I4, Uc4, h, m_Rp4)
            I2, Uc2 = second_order(t, I2, Uc2, h, m_Rp2)

        except:
            break

    do_plot(pltMasT, pltMasI4,  pltMasI2, 't',  'I', '4th order', '2nd order')
    do_plot(pltMasT, pltMasU4,  pltMasU2, 't', 'Uc', '4th order', '2nd order')
    do_plot(pltMasT, pltMasRp4, pltMasRp2, 't', 'Rp', '4th order', '2nd order')

    for i in range(len(pltMasI4)):
        pltMasI4[i] *= pltMasRp4[i]
        pltMasI2[i] *= pltMasRp2[i]

    do_plot(pltMasT, pltMasI4, pltMasI2, 't', 'Up', '4th order', '2nd order')
    do_plot(pltMasTzero, pltMasI4, pltMasI2, 't', 'T0', '4th order', '2nd order')

