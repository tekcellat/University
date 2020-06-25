from tkinter import *
from tkinter import messagebox
import math as m

#----------------------------------------
#Текс о программе
#----------------------------------------
text_prog = "Программа: Квадратное уровнение \n Решаеть любие квадратное уровнение. В программе данно 3 \
окошка и в каждой окошке нужна добавить цифру(букв, !, ? и т.п. нельзя добавить) \
и при нажатий кнопки [Решить] выводится окошка [Ответ], а при  нажатий меню \
[О разработчике] выводится информация о разработчике, а при нажати в меню \
[О программе] выводится информация о программе (то что вы сейчас читайте) \
Спасибо за внимание \n\n\n\n\n\n(21.02.2018)"
#----------------------------------------
#Текс о разработчике
#----------------------------------------
text_raz = "Автор: Гиёсов Фарухджон Нуриддинович \n\n\n\n\n\n(05.09.1999)"
#----------------------------------------
#
#решаеть квадратное уровнение
def farrukh():
     a = float(a_entry.get())
     b = float(b_entry.get())
     c = float(c_entry.get())
     
     d = (b * b - 4 * a * c)

     if a == 0  and b ==0 and c == 0:
          messagebox.showinfo("Ответ", "бесконечно много решений")
     if a == 0 and b == 0 and c != 0:
          messagebox.showinfo("Ответ", "Нет решений")
     if d < 0:
          messagebox.showinfo("Ответ", "Нет корней")
     elif d == 0 and a != 0:
         d = m.sqrt(d)
         x1 = (-b + d) / (2 * a)
         messagebox.showinfo("Ответ", "x1,x2 = " + str(round(x1, 3)))
     elif d > 0:
          if a == 0 and b != 0:
               x1 = -c / b
               messagebox.showinfo("Ответ", "x1 = " + str(round(x1, 3)))
          else:
               d = m.sqrt(d)
               x1 = (-b + d) / (2 * a)
               x2 = (-b - d) / (2 * a)
               messagebox.showinfo("Ответ", "x1 = " + str(round(x1, 3)) + "\n" + "x2 = " + str(round(x2, 3)))
def prog():
     messagebox.showinfo("О программе", text_prog)
def raz():
     messagebox.showinfo("О разработчике", text_raz)
def sterat():
     a_entry.delete(0, END)
     b_entry.delete(0, END)
     c_entry.delete(0, END)
#
root = Tk()
root.title("Квадратное уровнение")
#-------------------------------------------
#Меню "О программе" и "О Разработчике"
#-------------------------------------------
main_menu = Menu()

m_menu = Menu()
m_menu.add_command(label="О программе", command=prog)
m_menu.add_separator()
m_menu.add_command(label="О разработчике", command=raz)

main_menu.add_cascade(label="Меню", menu=m_menu)

root. config(menu=main_menu)
#--------------------------------------------

a = StringVar()
b = StringVar()
c = StringVar()
#
a_label = Label(text = " * x**2 + ")
b_label = Label(text = " * x + ")
c_label = Label(text = " = 0")
#
a_label.grid(row=0, column=1, sticky="w")
b_label.grid(row=0, column=3, sticky="w")
c_label.grid(row=0, column=5, sticky="w")
#
a_entry = Entry(textvariable=a)
b_entry = Entry(textvariable=b)
c_entry = Entry(textvariable=c)
#
a_entry.grid(row=0, column=0, padx=5, pady=5)
b_entry.grid(row=0, column=2, padx=5, pady=5)
c_entry.grid(row=0, column=4, padx=5, pady=5)

#кнопка Решить
message_button = Button(text="Решить", command=farrukh)
message_button.grid(row=2, column=6, padx=5, pady=5, sticky="w")

#кнопка стерать
message_button = Button(text="С", command=sterat)
message_button.grid(row=0, column=7, padx=5, pady=5, sticky="w")


root.mainloop()
