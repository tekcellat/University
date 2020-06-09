import matplotlib.pyplot as plt
import numpy as np

def draw_result(T_list_list, h_x, h_t):

    arg = []

    x_0 = 0

    for i in range(len(T_list_list[0])):
        arg.append(x_0)
        x_0 += h_x

    x = np.array(arg)
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

    for i in range(len(T_list_list)):
        y = np.array(T_list_list[i])
        plt.plot(x, y)

    plt.ylabel("T, К")
    plt.xlabel("x, см")

    plt.grid(True)

    plt.show()