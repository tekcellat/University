# Нахождение корней функции методом половинного деления.
# func - функция для исследования
# set_entries_bg - устанавливает цвет фона для указанных полей ввода
# get_interval - преобразует текстовое представление отрезка в два числа
# solve - как ни странно :)) решает заданную функцию


from tkinter import *
from math import *
import numpy as np
import matplotlib.pyplot as plt

def func(x):
    return sin(x)

def sign(x):
    if x < 0:
        return '-'
    else:
        return '+'

def float_output(x):
    eps = 0.000000001
    if fabs(round(x) - x) < eps:
        x = str(round(x))
    else:
        if fabs(x) < 0.000001:
            x = '%e' % x
        else:
            x = ('%.6f' % x).rstrip('0')
    return x

def set_entries_bg(color = 'red', *args):
    for i in args:
        i.config(bg = color)


def get_interval(interval):
    if len(interval) == 0:
        return
    if interval[0] == ']' and interval[-1] == '[':
        interval = interval[1:-1]
    interval = interval.split(' ')
    if len(interval) == 1:
        interval = interval[0].split(';')
    if len(interval) != 2:
        return
    try:
        a = float(interval[0].strip())
        b = float(interval[1].strip())
    except ValueError:
        return
    else:
        return (a, b)



def draw_plot(start, end, roots_x, roots_y):
    dx = 0.01
    
    xlist = list(np.arange(start, end, dx))
    ylist = [func(x) for x in xlist]

    min_x = []
    min_y = xlist[-1]
    max_x = []
    max_y = xlist[0]

    for i in range(len(xlist)):
        if ylist[i] < min_y:
            min_y = ylist[i]
        elif ylist[i] > max_y:
            max_y = ylist[i]

    for i in range(len(xlist)):
        if fabs(ylist[i] - min_y) < 0.001:
            min_x.append(xlist[i])
        elif fabs(ylist[i] - max_y) < 0.001:
            max_x.append(xlist[i])
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True, linestyle='-', color='0.75')
    
    plt.plot(xlist, ylist)
    plt.plot(roots_x, roots_y, 'go')
    plt.plot(min_x, [min_y] * len(min_x), 'ro')
    plt.plot(max_x, [max_y] * len(max_x), 'ro')
    
    plt.show()  

def find_roots(start, end, step, accuracy, max_iterations):
    N = 1
    max_func = func(start)
    min_func = max_func

    roots_x = []
    roots_y = []
    
    while start < end:
        next_ = start + step
        try:
            if sign(func(start)) != sign(func(next_)):
                
                iterations = 0
                a = start
                b = next_
                
                while b - a > accuracy and iterations < max_iterations:
                    if sign(func(a)) != sign(func(a + (b - a)/2)):
                        b = a + (b - a) / 2
                    else:
                        a = a + (b - a) / 2
                    iterations += 1
              
                
                if iterations < max_iterations:
                    x_text.insert(END, float_output(b) + '\n')
                    Fx_text.insert(END, float_output(func(b)) + '\n')
                    iterations_text.insert(END, '%d\n' % iterations)
                    error_text.insert(END, '0\n')
                    roots_x.append(b)
                    roots_y.append(func(b))

                else:
                    x_text.insert(END, '---\n')
                    Fx_text.insert(END, '---\n')
                    iterations_text.insert(END, '---\n')
                    error_text.insert(END, '1\n')
                intervals_text.insert(END,
                '[' + float_output(start) + ', ' +float_output(next_) + ']\n')
                N_text.insert(END, '%d\n' % N)
                N += 1
                    
        except ZeroDivisionError:
            x_text.insert(END, '---\n')
            Fx_text.insert(END, '---\n')
            iterations_text.insert(END, '---\n')
            error_text.insert(END, '2\n')
            
            intervals_text.insert(END,
            '[' + float_output(start) + ', ' +float_output(next_) + ']\n')
            N_text.insert(END, '%d\n' % N)
            N += 1
            
        start += step
    return roots_x, roots_y
    

def solve():
    plt.close()
    
    max_iterations = 1000
    interval = interval_entry.get()

    error = False
    
    try:
        start, end = get_interval(interval)
    except TypeError:
        set_entries_bg('red', interval_entry)
        error = True
    else:
        if end - start <= 0:
            set_entries_bg('red', interval_entry)
            error = True
    try:
        step = float(step_entry.get())
    except ValueError:
        set_entries_bg('red', step_entry)
        error = True
    else:
        if step >= end - start or step <= 0:
            set_entries_bg('red', step_entry)
            error = True

    try:
        accuracy = float(accuracy_entry.get())
    except ValueError:
        set_entries_bg('red', accuracy_entry)
        error = True
    else:
        if accuracy >= step or accuracy <= 0:
            set_entries_bg('red', accuracy_entry)
            error = True
            
    try:
        max_iterations = int(iterations_entry.get())
    except ValueError:
        set_entries_bg('red', iterations_entry)
        error = True
    else:
        if max_iterations <= 0:
            set_entries_bg('red', iterations_entry)
            error = True

    if error == True:
        return

    roots_x, roots_y = find_roots(start, end, step, accuracy, max_iterations)
    draw_plot(start, end, roots_x, roots_y)
    

# вывод окошка "о программе"
def about():
    def aquit():
        ab.destroy()
    ab = Toplevel(root)
    ab.grab_set()
    ab.resizable(False, False)
    ab.geometry("200x100")
    lab = Label(ab, text = '''Решение функций методом
половинного деления.''')
    ext = Button(ab, text = "Закрыть", command = aquit)
    lab.pack()
    ext.pack()
    ab.title('')

# вывод окошка "о программе"
def error_codes():
    ab = Toplevel(root)
    ab.grab_set()
    ab.resizable(False, False)
    ab.geometry("200x80")
    lab = Label(ab, text = '''0 - нет ошибки
1 - превышен лимит итераций
2 - деление на ноль''')
    lab.pack()
    ab.title('')

# настраиваем главное окно
root = Tk()
root.geometry("640x270")
root.title("Возможно тут должен быть заголовок.")
root.resizable(False, False)

# добавляем меню
m = Menu(root)
root.config(menu = m)
m.add_command(label="Расшифровка кодов ошибок", command = error_codes)
m.add_command(label="О программе", command = about)

# объявляем виджеты
N_label = Label(root, text = 'N')
intervals_label = Label(root, text = '[a, b]')
x_label = Label(root, text = 'x')
Fx_label = Label(root, text = 'F(x)')
iteration_label = Label(root, text = 'Итераций')
error_label = Label(root, text = 'Код ошибки')

interval_label = Label(root, text = 'Отрезок:')
step_label = Label(root, text = 'Шаг:')
accuracy_label = Label(root, text = 'Точность:')
iterations_label = Label(root, text = 'Итерации:')

interval_entry = Entry(root, width = 8)
step_entry = Entry(root, width = 8)
accuracy_entry = Entry(root, width = 8)
iterations_entry = Entry(root, width = 8)

N_text = Text(root, width = 2, height = 15)
intervals_text = Text(root, width = 15, height = 15)
x_text = Text(root, width = 13, height = 15)
Fx_text = Text(root, width = 13, height = 15)
iterations_text = Text(root, width = 7, height = 15)
error_text = Text(root, width = 10, height = 15)

solve_button = Button(root, text = 'Результат', command = solve)

# размещаем виджеты
N_label.grid(column=0, row=0)
N_text.grid(column=0, row=1, rowspan=15)
intervals_label.grid(column=1, row=0)
intervals_text.grid(column=1, row=1, rowspan=15)
x_label.grid(column=2, row=0)
x_text.grid(column=2, row=1, rowspan=15)
Fx_label.grid(column=3, row=0)
Fx_text.grid(column=3, row=1, rowspan=15)
iteration_label.grid(column=4, row=0)
iterations_text.grid(column=4, row=1, rowspan=15)
error_label.grid(column=5, row=0)
error_text.grid(column=5, row=1, rowspan=15)

interval_label.grid(column=6, row=1)
interval_entry.grid(column=7, row=1)
step_label.grid(column=6, row=2)
step_entry.grid(column=7, row=2)
accuracy_label.grid(column=6, row=3)
accuracy_entry.grid(column=7, row=3)
iterations_label.grid(column=6, row=4)
iterations_entry.grid(column=7, row=4)

solve_button.grid(column=7, row=5)
root.mainloop()
