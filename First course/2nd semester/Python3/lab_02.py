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


def sort_this():
    # Обработка сортировки и случайных ситуаций
    try:
        array = str(quest.get())
        if array[0] != "[":
            array = "[" + str(array)
        if array[-1] !="]":
            array = str(array) +"]"
        array2 = shellsort(eval(array))
        answer.insert(END, str(array2))
    except:
        answer.insert(END, "Неверный запрос")


def shellsort(array):
      def increment_generator(array):
          h = len(array)
          while h != 1:
              if h == 2:
                  h = 1
              else: 
                  h = 5*h//11
              yield h

      for increment in increment_generator(array):
          for i in range(increment, len(array)):
              for j in range(i, increment-1, -increment):
                  if array[j - increment] < array[j]:
                      break
                  array[j], array[j - increment] = array[j - increment], array[j]
      return array


# Считаем элементы для списков в случайном порядке
def Random_List(koeficient):
    List = []
    for i in range(koeficient):
        List.append(random.randrange(0, koeficient, 1))
    return List
# Подсчёт времени
def Count_Time(List):
    start_time = time.clock()
    shellsort(List)
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

win = Tk()
win.title("Сортировка методом Шелла")
win_width = '780'
win_height = '200'
win.maxsize(width=win_width,height=win_height)
win.minsize(width=win_width,height=win_height)


frame1 = Frame(win)
frame1.pack(side="top")
quest = Entry(frame1,width=20, font='Arial 14', bd=5)
quest.pack(side="left")
sort_button = Button(frame1, text='==>', width=4, height=1, bg='lightblue', font='arial 14', command=sort_this)
sort_button.pack(side="left")
answer = Entry(frame1, state='normal', width=20, font='Arial 14', bd=5)
answer.pack(side="left")


table = Table(win, headings=('Lalalala', '100 elements', '1000 elements', '10000 elements'),
              rows=(('Increasing', out_list[0], out_list[1],out_list[2]),
                    ('Decreasing', out_list[3], out_list[4],out_list[5]),
                    ('Random', out_list[6], out_list[7],out_list[8])))
table.pack(expand=YES, fill=BOTH)


# выключаем возможность изменять окно
win.resizable(width=False, height=False)
win.mainloop()
