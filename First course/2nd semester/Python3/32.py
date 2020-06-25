from tkinter import *
from tkinter import messagebox
import random

root = Tk()
root.title("dfvdfvdf")

def farrukh():
    # Обработка сортировки и случайных ситуаций
    try:
        array = str(a_entry.get())
        if array[0] != "[":
            array = "[" + str(array)
        if array[-1] !="]":
            array = str(array) +"]"
        print(array)
        array2 = Shaker_Sort(eval(array))
        a.delete(0, END)
        a.insert(END, str(array2))
    except:
        a.delete(0, END)
        a.insert(END, "Неверный запрос")

a = StringVar()
#
a_entry = Entry(textvariable=a)
#
a_entry.grid(row=1, column=1, columnspan=3, sticky='nsew', padx=5, pady=5)
#
a = Entry(text="Ответ")
a.grid(row=2, column=1, columnspan=1, padx=5, pady=5, sticky="w")
#кнопка Решить
button1 = Button(text="Решить", command=farrukh)
button1.grid(row=2, column=4, columnspan=1, padx=5, pady=5, sticky="w")
