import numpy as np
from math import cos

def nearest_number(lst, x):
    a = 0
    b = len(lst) - 1
    while a < b:
        m = int((a + b) / 2)
        if x < lst[m]:
            a = m + 1
        else:
            b = m
    return b

def function_recursion(x, y):
    l = len(x)
    if l == 1:
        return y[0]
    else:
        return (function_recursion(x[:-1], y[:-1]) - function_recursion(x[1:], y[1:])) / (x[0] - x[l - 1])

def newton_interpolation():
    all_x, all_y = create_table()
    print_table(all_x, all_y)
    x = float(input('y: '))
    n = int(input('n: '))
    
    nearest = nearest_number(all_x, x)
    if len(all_x) < nearest + (n + 1) / 2:
        near_x = all_x
        near_y = all_y
    else:
        if n % 2 != 0:
            near_x = all_x[nearest - int((n + 1) / 2): nearest + int((n + 1) / 2)]
            near_y = all_y[nearest - int((n + 1) / 2): nearest + int((n + 1) / 2)]
        else:
            near_x = all_x[nearest - int((n + 1) / 2) - 1: nearest + int((n + 1) / 2)]
            near_y = all_y[nearest - int((n + 1) / 2) - 1: nearest + int((n + 1) / 2)]
    y_result = near_y[0]

    for i in range(1, len(near_x)):
        k = 1
        for j in range(i):
            k *= (x - near_x[j])
        function = function_recursion(near_x[:i+1], near_y[:i+1])
        y_result += (k * function)
    return y_result

def func(x):
    return x*x-4

def create_table():
    x = []
    y = []
    for current_x in np.arange(-4, 1, 1):
        y.append(current_x)
        x.append(func(current_x))
    return x, y

def print_table(x, y):
    print('\n\ny          x')
    for i in range(len(x)):
        print('{}     {}'.format(x[i], y[i]))
    print('\n')

my_result = newton_interpolation()

print('Result: {}'.format(my_result))
