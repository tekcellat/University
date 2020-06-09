from print_graph import draw_result, draw_dots, draw_table, draw_results_by_one_x
from task import solve_task
from data import Data
import numpy as np

def data_init():
    data = Data()
    return data


def print_constants(data):
    print("a_1 : " + str(data.a_1))
    print("b_1 : " + str(data.b_1))
    print("c_1 : " + str(data.c_1))
    print("m_1 : " + str(data.m_1))
    print("a_2 : " + str(data.a_2))
    print("b_2 : " + str(data.b_2))
    print("c_2 : " + str(data.c_2))
    print("m_2 : " + str(data.m_2))
    print("alpha_0 : " + str(data.alpha_0))
    print("alpha_N : " + str(data.alpha_N))
    print("l : " + str(data.l))
    print("T_0 : " + str(data.T_0))
    print("R : " + str(data.R))
    print("F_0 : " + str(data.F_0))
    print("eps : " + str(data.eps))


def print_menu():
    print("Выберите действие: ")
    print("1. Сменить F_0")
    print("0. Настройка завершена")
    return int(input())


def change_value(data, str):
    new_value = float(input("Введите " + str + ": "))
    if (str == "F_0"):
        data.F_0 = new_value


def calc_int(data, T_list_list):
    result = 0

    for i in T_list_list[-1]:
        result += i - data.T_0

    return result


def check_result(result, data):
    F_N = data.alpha_N * (result[-1][-1] - data.T_0)
    eps = 10e-2
    return ((data.F_0 - F_N) / (2 * data.alpha_N / data.R * calc_int(data, result)) - 1) <= eps

if __name__ == '__main__':
    data = data_init()

    while(True):
        print_constants(data)

        choice = print_menu()

        if (choice == 0):
            break
        elif (choice == 1):
            change_value(data, "F_0")


    h_t = float(input("Введите шаг по времени: "))

    h_x = float(input("Введите шаг по длине стержня: "))

    t_max = float(input("Введите время, до которого будет считать программа: "))

    frequency = float(input("Введите частоту, с которой будут посылаться импульсы, с: "))

    #цикл шагов по времени
    '''
    h_count = []
    for t in np.arange(1, 10, 1):
        for x in np.arange(0.1, 1, 0.1):
            result = solve_task(data, x, t, t_max)
            if (check_result(result, data)):
                h_count.append([x, t])
    '''

    #a_2_list = [data.a_2, 3, 4, 5]
    #result = []
    #result.append(solve_task(data, h_x, h_t, t_max))
    #data.a_2 = a_2_list[1]
    #result.append(solve_task(data, h_x, h_t, t_max))
    #data.a_2 = a_2_list[2]
    #result.append(solve_task(data, h_x, h_t, t_max))
    #data.a_2 = a_2_list[3]
    #result.append(solve_task(data, h_x, h_t, t_max))

    #draw_results_by_one_x(result, h_x, h_t, a_2_list)

    result = solve_task(data, h_x, h_t, t_max, frequency)

    print(len(result))

    draw_result(result, h_x, h_t)

    #draw_dots(h_count)


    #T_list_list_0_3 = solve_task(data, 0.3, h_t, t_max)
    #T_list_list_0_1 = solve_task(data, 0.1, h_t, t_max)
    #T_list_list_0_05 = solve_task(data, 0.05, h_t, t_max)
    #T_list_list_0_01 = solve_task(data, 0.01, h_t, t_max)
    #T_list_list_0_005 = solve_task(data, 0.005, h_t, t_max)
    #T_list_list_0_001 = solve_task(data, 0.001, h_t, t_max)

    #draw_table(T_list_list_0_3, T_list_list_0_1, T_list_list_0_05, T_list_list_0_01, T_list_list_0_005, T_list_list_0_001, 0.3, h_t)