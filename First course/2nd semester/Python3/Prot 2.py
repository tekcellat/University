from tkinter import *
import tkinter as tk

def sort_this():
    try:
        array = str(quest.get())
        if array[0] != "[":
            array = "[" + str(array)
        if array[-1] !="]":
            array = str(array) +"]"
        array2 = your_sort(eval(array))
        answer.insert(END, str(array2))
        
    except:
        answer.insert(END, "Неверный запрос")

def your_sort(array):
    #in here write logic of your method
    return array

win = Tk()
win.title("Сортировка методом ####")
frame = Frame(win)
frame.pack(side="top")
quest = Entry(frame,width=20, font='Arial 14', bd=5)
quest.grid(row=1,column =5)
sort_button = Button(frame, text='Sort', width=4, height=1, font='arial 14', command=sort_this)
sort_button.grid(row=4, column=5)
answer = Entry(frame, width=20, font='Arial 14', bd=5)
answer.grid(row=2, column=5)
win.mainloop()