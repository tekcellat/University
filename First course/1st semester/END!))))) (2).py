# Из заданного множества точек на плоскости выбрать две различные точки так,
# чтобы количества точек, лежащих по разные стороны прямой, проходящей через
# эти две точки, различались наименьшим образом.

import matplotlib.pyplot as plt
import numpy as np

def is_float(x):
    dot = 0
    minus = 0
    e = 0
    for i in range(len(x)):
        if x[i] == '-':
            if minus == 0:
                minus == 1
            else:
                return False
        if x[i] == '.':
            if e == 0 and dot == 0:
                dot = 1
            else:
                return False
        if x[i] == 'e':
            if e == 0 and i > 0:
                e = 1
            else:
                return False
    return True


while True:
    n = input("Введите количество точек: ")
    if n.isdigit():
        n = int(n)
        break
    else:
        print("Количество точек должно быть целым положительным числом.")

dots = []
for i in range(n):
    while True:
        s = input("Введите координаты точки: ")
        if len(s.split()) == 2:
            x, y = s.split()
        else:
            print('Вы должны ввести 2 числа.')
            continue        
        if is_float(x) and is_float(y):
            dots.append((float(x), float(y)))
            break
        else:
            print("Координаты точек должны быть вещественными числами.")

# Нахождение искомой прямой.
delta = n
dot1 = dot2 = None
for i in range(len(dots)):
    for j in range(i, len(dots)):
        if dots[i] != dots[j]:
            dots_left = 0
            dots_right = 0
            for dot in dots:
                if dot != dots[i] and dot != dots[j]:
                    s = (dots[j][0] - dots[i][0]) * (dot[1] - dots[i][1]) -\
                        (dots[j][1] - dots[i][1]) * (dot[0] - dots[i][0])
                    if s > 0:
                        dots_left += 1
                    if s < 0:
                        dots_right += 1
            if abs(dots_right - dots_left) < delta:
                delta = abs(dots_right - dots_left)
                dot1 = dots[i]
                dot2 = dots[j]
                
print('\nИскомая прямая проходит через точки: ({:.2f};{:.2f}), ({:.2f};{:.2f})'
      .format(dot1[0], dot1[1], dot2[0], dot2[1]))

# Нахождение отрезка, на котором будет строиться искомая прямая.
x0 = dots[0][0]
x1 = dots[0][0]
y0 = dots[0][1]
y1 = dots[0][1]
for dot in dots:
    if dot[0] < x0:
        x0 = dot[0]
    if dot[0] > x1:
        x1 = dot[0]
    if dot[1] < y0:
        y0 = dot[1]
    if dot[1] > y1:
        y1 = dot[1]
if dot1[0] != dot2[0]:
    x = np.linspace(x0-1, x1+1) 
    y = (x - dot1[0])*(dot2[1] - dot1[1])/(dot2[0] - dot1[0]) + dot1[1]
else:
    y = np.linspace(y0-1, y1+1)
    x = [dot1[0]]*len(y)

# Построение точек.
fig = plt.figure()
for dot in dots:
    plt.scatter(dot[0], dot[1])

# Построение искомой прямой.
plt.plot(x, y)

plt.subplot().spines['left'].set_position('zero')
plt.subplot().spines['bottom'].set_position('zero')
plt.grid(True)
plt.subplots_adjust(hspace=0.1, wspace=0.1)
plt.show()
