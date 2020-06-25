import time
import random
from tkinter import *
import tkinter.ttk as ttk


class Table(Frame):
    # Параметры для таблицы
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"]=headings
        table["displaycolumns"]=headings

        for head in headings:
            table.heading(head, text=head, anchor=CENTER)
            table.column(head, anchor=CENTER)

        for row in rows:
            table.insert('', END, values=tuple(row))

        scrolltable = Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=RIGHT, fill=Y)
        table.pack(expand=YES, fill=BOTH)


def back():
    # Стереть последний введённый символ
    quest.delete(len(quest.get()) - 1, END)


def action_delete():
    # Очистка всех полей
    quest.delete(0, END)
    answer.delete(0, END)


def sort_this():
    # Обработка сортировки и случайных ситуаций
    try:
        array = str(quest.get())
        if array[0] != "[":
            array = "[" + str(array)
        if array[-1] !="]":
            array = str(array) +"]"
        print(array)
        array2 = Shaker_Sort(eval(array))
        answer.delete(0, END)
        answer.insert(END, str(array2))
    except:
        answer.delete(0, END)
        answer.insert(END, "Неверный запрос")


def Shaker_Sort(array):
    # Шейкерная сортировка
    swapped = True
    rb = len(array)
    lb = 0
    while swapped == True and lb <= rb:
        swapped = False
        k = 0
        # Идем вперед
        for i in range(lb, rb - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
                k = i + 1
        rb = k
        # Возвращаемся назад
        for i in range(rb, lb, -1):
            if array[i] < array[i - 1]:
                array[i - 1], array[i] = array[i], array[i - 1]
                swapped = True
                k = i - 1
        lb = k
    return array


def Random_List(koeficient):
    # Считаем элементы для списков в случайном
    List = []
    for i in range(koeficient):
        List.append(random.randrange(0, koeficient, 1))
    return List


def Count_Time(List):
    # Подсчёт времени
    start_time = time.clock()
    Shaker_Sort(List)
    stop_time = time.clock() - start_time
    return round(stop_time, 10)


# Создание массивов
mass_100 = list(range(0, 100))
mass_1000 = list(range(0, 1000))
mass_10000 = list(range(0, 10000))

mass_backward_100 = [x for x in range(99, 0, -1)]
mass_backward_1000 = [x for x in range(999, 0, -1)]
mass_backward_10000 = [x for x in range(9999, 0, -1)]

mass_random_100 = Random_List(100)
mass_random_1000 = Random_List(1000)
mass_random_10000 = Random_List(10000)

# Создание списка замеров времени для вывода
out_list = []
out_list.append(Count_Time(mass_100))
out_list.append(Count_Time(mass_1000))
out_list.append(Count_Time(mass_10000))
out_list.append(Count_Time(mass_backward_100))
out_list.append(Count_Time(mass_backward_1000))
out_list.append(Count_Time(mass_backward_10000))
out_list.append(Count_Time(mass_random_100))
out_list.append(Count_Time(mass_random_1000))
out_list.append(Count_Time(mass_random_10000))

# Печать таблицы
print("|---------------------------------------------------------------|")
print("|                             Table                             |")
print("|               |-------------------------------|---------------|")
print("|               | 100 elements  | 1000 elements | 10000 elements|")
print("|---------------|---------------|---------------|---------------|")
print("| Increasing    | {:.11f} | {:.11f} | {:.11f} |".format(out_list[0], out_list[1],out_list[2]))
print("|---------------|---------------|---------------|---------------|")
print("| Decreasing    | {:.11f} | {:.11f} | {:.10f} |".format(out_list[3], out_list[4],out_list[5]))
print("|---------------|---------------|---------------|---------------|")
print("| Random        | {:.11f} | {:.11f} | {:.10f} |".format(out_list[6], out_list[7],out_list[8]))
print("|---------------|---------------|---------------|---------------|")

win = Tk()
win.title("Тестировка шейкер-сортировки")

frame1 = Frame(win)
frame1.pack(side="top")
quest = Entry(frame1,width=20, font='Arial 14', bg="lightgray", bd=5)
quest.pack(side="left")
back_button = Button(frame1, text='<', width=3, height=2, font='arial 14', command=back)
back_button.pack(side="right")
sort_button = Button(frame1, text='Sort this', width=6, height=2, bg='green', font='arial 14', command=sort_this)
sort_button.pack(side="left")
answer = Entry(frame1, state='normal', width=20, font='Arial 14', bg="lightgray", bd=5)
answer.pack(side="left")
delete_button = Button(frame1, text='clear', width=3, height=2, bg='black', fg='red', font='arial 14', command=action_delete)
delete_button.pack(side="left")

table = Table(win, headings=('', '100 elements', '1000 elements', '10000 elements'),
              rows=(('Increasing', out_list[0], out_list[1],out_list[2]),
                    ('Decreasing', out_list[3], out_list[4],out_list[5]),
                    ('Random', out_list[6], out_list[7],out_list[8])))
table.pack(expand=YES, fill=BOTH)
win.mainloop()