import matplotlib.pyplot as plt
import numpy as np
from math import *
from prettytable import PrettyTable

def get_T_list_for_cur_x(T_list_list, x, h_x):
    i = int(x / h_x)
    result = []
    for T_list in T_list_list:
        result.append(T_list[i])
    return result


def draw_results_by_one_x(result_list, h_x, h_t, a_2_list):
    arg = []

    x_0 = 0

    for i in range(len(result_list[0])):
        arg.append(x_0)
        x_0 += h_t

    x = np.array(arg)

    for i in range(len(result_list)):
        y = np.array(get_T_list_for_cur_x(result_list[i], 0, h_x))
        plt.plot(x, y, label=('b_2 = 0.563e-3; a_2 = ' + str(a_2_list[i])))
        plt.legend()

    plt.ylabel("T, К")
    plt.xlabel("t, с")

    plt.grid(True)

    plt.show()

def draw_result(T_list_list, h_x, h_t):

    arg = []

    x_0 = 0
    '''
    for i in range(len(T_list_list[0])):
        arg.append(x_0)
        x_0 += h_x
    '''
    for i in range(len(T_list_list)):
        arg.append(x_0)
        x_0 += h_t

    x = np.array(arg)
    '''
    plt.plot(x, np.array(get_T_list_for_cur_x(T_list_list, 0, h_x)))
    plt.plot(x, np.array(get_T_list_for_cur_x(T_list_list, 0.15, h_x)))
    plt.plot(x, np.array(get_T_list_for_cur_x(T_list_list, 0.3, h_x)))
    plt.plot(x, np.array(get_T_list_for_cur_x(T_list_list, 0.5, h_x)))
    plt.plot(x, np.array(get_T_list_for_cur_x(T_list_list, 1.0, h_x)))
    plt.plot(x, np.array(get_T_list_for_cur_x(T_list_list, 1.5, h_x)))
    plt.plot(x, np.array(get_T_list_for_cur_x(T_list_list, 2.0, h_x)))
    plt.plot(x, np.array(get_T_list_for_cur_x(T_list_list, 9.99, h_x)))
    '''
    '''
    plt.plot(x, np.array(T_list_list[0]))
    plt.plot(x, np.array(T_list_list[1]))
    plt.plot(x, np.array(T_list_list[2]))
    plt.plot(x, np.array(T_list_list[3]))
    plt.plot(x, np.array(T_list_list[4]))
    plt.plot(x, np.array(T_list_list[5]))

    plt.plot(x, np.array(T_list_list[12]))

    plt.plot(x, np.array(T_list_list[-1]))
    '''

    '''
    for i in range(len(T_list_list)):
        y = np.array(T_list_list[i])
        plt.plot(x, y)
    '''

    y = np.array(get_T_list_for_cur_x(T_list_list, 0, h_x))
    plt.plot(x, y, label = ('x = 0'))
    plt.legend()


    '''
    #Вывод графиков логарифмически
    count = int(floor(log(len(T_list_list), 2)))
    for i in range(count + 1):
        y = np.array(T_list_list[2 ** i])
        plt.plot(x, y, label=('t = ' + str(2 ** i * h_t) + ' c'))
        plt.legend()

    y = np.array(T_list_list[-1])
    plt.plot(x, y, label=('t = ' + str((len(T_list_list) - 1) * h_t) + ' с'))
    plt.legend()
    '''
    '''
    t_value_list = [18, 36, 72, 144, 180]
    for t_value in t_value_list:
        y = np.array(T_list_list[int(t_value / h_t)])
        plt.plot(x, y, label=('t = ' + str(t_value) + ' c'))
        plt.legend()
    '''

    plt.ylabel("T, К")
    plt.xlabel("t, с")

    plt.grid(True)

    plt.show()

def draw_dots(h_count):
    fig = plt.figure()
    for i in range(len(h_count)):
        plt.scatter(h_count[i][0], h_count[i][1])
    plt.ylabel("t, c")
    plt.xlabel("x, см")
    plt.grid(True)
    plt.show()

def print_table(t_value_list, T_list_list_9, T_list_list_6, T_list_list_3, T_list_list_1, T_list_list_0_5, T_list_list_0_25, h_x):
    x = PrettyTable()
    T_t = "T(t_i=" + str(t_value_list) + "с), tau = "
    x.field_names = ["x,см", T_t + str(9) + "с",
                     T_t + str(6) + "с",
                     T_t + str(3) + "с",
                     T_t + str(1) + "с",
                     T_t + str(0.5) + "с",
                     T_t + str(0.25) + "с"]

    x_0 = 0
    for i in range(len(T_list_list_1[0])):
        x.add_row(["{:8.2f}".format(x_0), "{:8.4f}".format(T_list_list_9[int(t_value_list / 9)][i]),
                   "{:8.4f}".format(T_list_list_6[int(t_value_list / 6)][i]),
                   "{:8.4f}".format(T_list_list_3[int(t_value_list / 3)][i]),
                   "{:8.4f}".format(T_list_list_1[int(t_value_list / 1)][i]),
                   "{:8.4f}".format(T_list_list_0_5[int(t_value_list / 0.5)][i]),
                   "{:8.4f}".format(T_list_list_0_25[int(t_value_list / 0.25)][i])])
        x_0 += h_x

    print(x)


def print_table_2(t_value_list,
                T_list_list_0_3,
                T_list_list_0_1,
                T_list_list_0_05, T_list_list_0_01, T_list_list_0_005, T_list_list_0_001, h_x, h_t):
    x = PrettyTable()
    T_t = "T(t_i=" + str(t_value_list) + "с),h="
    x.field_names = ["x,см", T_t + str(0.3) + "см",
                     T_t + str(0.1) + "см",
                     T_t + str(0.05) + "см",
                     T_t + str(0.01) + "см",
                     T_t + str(0.005) + "см",
                     T_t + str(0.001) + "см"]

    x_0 = 0
    for i in range(len(T_list_list_0_3[0])):
        x.add_row(["{:8.2f}".format(x_0),
                   "{:8.4f}".format(T_list_list_0_3[int(t_value_list / h_t)][int(x_0 / 0.3)]),
                   "{:8.4f}".format(T_list_list_0_1[int(t_value_list / h_t)][int(x_0 / 0.1)]),
                   "{:8.4f}".format(T_list_list_0_05[int(t_value_list / h_t)][int(x_0 / 0.05)]),
                   "{:8.4f}".format(T_list_list_0_01[int(t_value_list / h_t)][int(x_0 / 0.01)]),
                   "{:8.4f}".format(T_list_list_0_005[int(t_value_list / h_t)][int(x_0 / 0.005)]),
                   "{:8.4f}".format(T_list_list_0_001[int(t_value_list / h_t)][int(x_0 / 0.001)])])
        x_0 += h_x

    print(x)

def draw_table(T_list_list_9, T_list_list_6, T_list_list_3, T_list_list_1, T_list_list_0_5, T_list_list_0_25, h_x, h_t):
    t_value_list = [18, 36, 72, 144]

    print_table_2(t_value_list[0], T_list_list_9, T_list_list_6, T_list_list_3, T_list_list_1, T_list_list_0_5, T_list_list_0_25, h_x, h_t)
    print_table_2(t_value_list[1], T_list_list_9, T_list_list_6, T_list_list_3, T_list_list_1, T_list_list_0_5, T_list_list_0_25, h_x, h_t)
    print_table_2(t_value_list[2], T_list_list_9, T_list_list_6, T_list_list_3, T_list_list_1, T_list_list_0_5, T_list_list_0_25, h_x, h_t)
    print_table_2(t_value_list[3], T_list_list_9, T_list_list_6, T_list_list_3, T_list_list_1, T_list_list_0_5, T_list_list_0_25, h_x, h_t)
