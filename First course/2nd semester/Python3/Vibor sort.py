import time
import random
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

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
        #scrolltable.pack(side=RIGHT, fill=Y)
        table.pack(expand=YES, fill=BOTH)

def sorting():
    try:
        array = str(quest.get())
        if array[0] != "[":
            array = "[" + str(array)
        if array[-1] !="]":
            array = str(array) +"]"
        array2 = mysort(eval(array))
        answer.insert(END, str(array2))
        
    except:
        answer.insert(END, "Input only int")

def mysort(array): 
    for i in range(0, len(array) - 1): 
        min_idx = i 
        for j in range(i + 1, len(array)): 
            if array[j] < array[min_idx]: 
                min_idx = j 
        array[i], array[min_idx] = array[min_idx], array[i]
    return array
    
def Random_List(koeficient):
    List = []
    for i in range(koeficient):
        List.append(random.randrange(0, koeficient, 1))
    return List

def Count_Time(List):
    start_time = time.clock()
    mysort(List)
    stop_time = time.clock() - start_time
    return round(stop_time, 10)

def random_arr_input():
    try:
        a_val= int(a.get())
        b_val= int(b.get())
        c_val= int(c.get())
        random_arr(a_val,b_val,c_val)
    except:
        messagebox.showinfo("ERROR", "Input only int")

def random_arr(a,b,c):
    mass_a = random.sample(range(a), a)
    mass_b = random.sample(range(b), b)
    mass_c = random.sample(range(c), c)
    mass_backward_a = [x for x in range(a)]
    mass_backward_b = [x for x in range(b)]
    mass_backward_c = [x for x in range(c)]
    mass_random_a = Random_List(a)
    mass_random_b = Random_List(b)
    mass_random_c = Random_List(c)

    out_list = []
    out_list.append(Count_Time(mass_a))
    out_list.append(Count_Time(mass_b))
    out_list.append(Count_Time(mass_c))
    out_list.append(Count_Time(mass_backward_a))
    out_list.append(Count_Time(mass_backward_b))
    out_list.append(Count_Time(mass_backward_c))
    out_list.append(Count_Time(mass_random_a))
    out_list.append(Count_Time(mass_random_b))
    out_list.append(Count_Time(mass_random_c))

    table = Table(win, headings=('       ', 'Arrive a', 'Arrive b', 'Arrive c'),
            rows=(('Increasing', out_list[0], out_list[1],out_list[2]),
                    ('Decreasing', out_list[3], out_list[4],out_list[5]),
                    ('Random', out_list[6], out_list[7],out_list[8])))
    table.pack(expand=YES, fill=BOTH)

win = Tk()
win.title("Sort by viborom")
frame = Frame(win)
frame.pack(side="top")
quest = Entry(frame,width=20, font='Arial 14',bg='lightgrey', bd=5)
quest.grid(row=1,column =5)
a = Entry(frame,width=4, font='Arial 14', bd=4)
a.grid(row = 1, column=2)
b = Entry(frame,width=4, font='Arial 14', bd=4)
b.grid(row = 1, column=4)
c = Entry(frame,width=4, font='Arial 14', bd=4)
c.grid(row = 2, column=2)
sort_button = Button(frame, text='Sorting', width=6, height=1, font='arial 14',bg='lightgreen', command=sorting)
sort_button.grid(row=4, column=5)
but = Button( frame, text = 'Arrive',command = random_arr_input).grid(row = 2, column = 4)
answer = Entry(frame, width=20,bg='lightgrey', font='Arial 14', bd=5)
answer.grid(row=2, column=5)
win.mainloop()