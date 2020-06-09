from progonka import *
from math import *
import numpy as np


def get_abs_dif(y_n_s_minus_1, y_n_s):
    return fabs((y_n_s - y_n_s_minus_1) / y_n_s)

def get_max_dif_from_result(T_list, T_new_list):
    max_dif = 0
    for i in range(len(T_list)):
        dif = get_abs_dif(T_list[i], T_new_list[i])
        if (max_dif < dif):
            max_dif = dif
    return max_dif



def calc_A_n(T_n, T_n_plus_1, data, h_x, h_t):
    return data.X_n_and_half(T_n, T_n_plus_1) * h_t / h_x


def calc_C_n(T_n, T_n_minus_1, data, h_x, h_t):
    return data.X_n_and_half(T_n, T_n_minus_1) * h_t / h_x


def calc_B_n(T_n, data, A, C, h_x, h_t, cur_x):
    return A + C + data.c_T(T_n) * h_x + data.p_x(cur_x) * h_x * h_t

def calc_F_n(T_n, data, h_x, h_t, cur_x, T_time_ago):
    return data.f_x(cur_x) * h_x * h_t + data.c_T(T_n) * T_time_ago * h_x

def calc_coeff(data, T_list, h_x, h_t, T_time_ago_list):
    A_list, B_list, C_list, F_list = [], [], [], []

    for i in range(1, len(T_list) - 1):
        cur_x = i * h_x

        A = calc_A_n(cur_x, cur_x + h_x, data, h_x, h_t)

        C = calc_C_n(cur_x, cur_x - h_x, data, h_x, h_t)

        #A = calc_A_n(T_list[i], T_list[i + 1], data, h_x, h_t)

        #C = calc_C_n(T_list[i], T_list[i - 1], data, h_x, h_t)

        B = calc_B_n(T_list[i], data, A, C, h_x, h_t, cur_x)
        F = calc_F_n(T_list[i], data, h_x, h_t, cur_x, T_time_ago_list[i])

        A_list.append(A)
        C_list.append(C)
        B_list.append(B)
        F_list.append(F)

    return A_list, B_list, C_list, F_list


def get_sum_from_all_pulses(data, t):
    sum_F_t = data.F_t(t)
    for pulse_t in data.t_list:
        sum_F_t += data.F_t(pulse_t)
    return sum_F_t

def calc_left_condition(data, T_list, h_x, h_t, T_old_list, t):
    c_0 = data.c_T(T_list[0])
    c_1 = data.c_T(T_list[1])
    p_0 = data.p_x(0)
    p_1 = data.p_x(h_x)
    p_half = (p_0 + p_1) / 2
    c_half = (c_0 + c_1) / 2
    X_half = data.X_n_and_half(0, h_x)
    #X_half = data.X_n_and_half(T_list[0], T_list[1])
    y_0 = T_old_list[0]
    y_1 = T_old_list[1]
    f_0 = data.f_x(0)
    f_1 = data.f_x(h_x)
    f_half = (f_0 + f_1) / 2

    F_t = get_sum_from_all_pulses(data, t)

    K_0 = h_x * (c_half / 8 +
                 (c_0 / 4) +
                 (h_t * p_half / 8) +
                 (h_t * p_0 / 4)) + \
          X_half * h_t / h_x

    M_0 = h_x * c_half / 8 - \
          X_half * h_t / h_x + \
          h_t * h_x * p_half / 8

    P_0 = h_x * (
        c_half * (y_0 + y_1) / 8 +
        c_0 * y_0 / 4 +
        h_t * (f_half + f_0) / 4
    ) + F_t * h_t

    return K_0, M_0, P_0

def calc_right_condition(data, T_list, h_x, h_t, T_old_list):
    N = len(T_list)
    c_N = data.c_T(T_list[N - 1])
    c_N_minus_1 = data.c_T(T_list[N - 2])
    p_N = data.p_x(data.l)
    p_N_minus_1 = data.p_x(data.l - h_x)
    p_N_minus_half = (p_N + p_N_minus_1) / 2
    c_N_minus_half = (c_N + c_N_minus_1) / 2
    X_N_minus_half = data.X_n_and_half(data.l, data.l - h_x)
    #X_N_minus_half = data.X_n_and_half(T_list[N - 1], T_list[N - 2])
    y_N = T_old_list[N - 1]
    y_N_minus_1 = T_old_list[N - 2]
    f_N = data.f_x(data.l)
    f_N_minus_1 = data.f_x(data.l - h_x)

    K_N = h_t * (X_N_minus_half / h_x + data.alpha_N + h_x / 4 * p_N + h_x / 8 * p_N_minus_half) +\
          h_x * c_N / 4 + h_x * c_N_minus_half / 8

    M_N = - h_t * (X_N_minus_half / h_x - h_x * p_N_minus_half / 8) +\
          h_x * c_N_minus_half / 8

    P_N = data.alpha_N * data.T_0 * h_t +\
          h_t * h_x * (3 * f_N + f_N_minus_1) / 8 +\
        h_x * c_N * y_N / 4 +\
        h_x * c_N_minus_half * (y_N + y_N_minus_1) / 8


    return K_N, M_N, P_N


def get_T_list_for_cur_time(data, T_old_list, h_x, h_t, t):

    T_list = T_old_list
    max_dif = 1

    while (max_dif > data.eps):

        A_list, B_list, C_list, F_list = calc_coeff(data, T_list, h_x, h_t, T_old_list)

        K_0, M_0, P_0 = calc_left_condition(data, T_list, h_x, h_t, T_old_list, t)

        K_N, M_N, P_N = calc_right_condition(data, T_list, h_x, h_t, T_old_list)

        T_new_list = progonka(A_list, B_list, C_list, F_list, K_0, M_0, P_0, K_N, M_N, P_N)

        max_dif = get_max_dif_from_result(T_list, T_new_list)

        T_list = T_new_list

    return T_list


def solve_task(data, h_x, h_t, t_max, frequency):

    T_list_list = []

    T_base_list = [data.T_0 for i in np.arange(0, data.l, h_x)]

    max_dif = 1

    T_list_list.append(T_base_list)

    period = 1 / frequency

    #цикл по времени
    t = h_t
    sum_t = t
    while (True):
        if (t >= period):
            data.t_list.append(t)
            t = 0
        T_new_list = get_T_list_for_cur_time(data, T_base_list, h_x, h_t, t)
        T_list_list.append(T_new_list)

        #max_dif = get_max_dif_from_result(T_base_list, T_new_list)

        T_base_list = T_new_list
        data.t_list_update(h_t)
        t += h_t
        sum_t += h_t

        check = data.F_t(sum_t) / data.F_max
        if (check < 0.05):
            print("F(t_u)/F_max: " + str(check))
            print("t_u: " + str(sum_t) + "\n")

        if (sum_t > t_max):
            break

    return T_list_list