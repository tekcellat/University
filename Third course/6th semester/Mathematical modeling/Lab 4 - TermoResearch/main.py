from print_graph import draw_result
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

    result = solve_task(data, h_x, h_t)

    print(result[-1])

    draw_result(result, h_x, h_t)