from tkinter import *
from tkinter import messagebox


#Из двочной в десятичную
def twte():
    try: 
        n=int(a_entry.get())
        if n > 0:
            s=str(int(str(n),2))
            messagebox.showinfo("Ответ", s)
        else:
            messagebox.showinfo("ERROR", "Вводите правильно")
    except:
        messagebox.showinfo("ERROR", "Вводите правильно")
#Из десятичной в двоичную
def tetw():
    try:
        x = int(b_entry.get())
        if x > 0 and int:
            n = ""
            while x > 0:
                y = str(x % 2)
                n = y + n
                x = int(x / 2)
            messagebox.showinfo("Ответ", n)
        else:
            messagebox.showinfo("ERROR", "Вводите правильно")
    except:
            messagebox.showinfo("ERROR", "Вводите правильно")


#Очистка полей ввода
def delete():
     a_entry.delete(0, END)
     b_entry.delete(0, END)


#окно
root = Tk()
root.title("2/10 or 10/2")

#Мессажи
def print_program_info():
    messagebox.showinfo('Info','Перевод c 2с/с в 10с/с и обратно')

def print_author():
    messagebox.showinfo('Author','Hasanzade M.A.')


#Menu
main_menu = Menu()
m_menu = Menu()

m_menu.add_cascade(label='Program info',command=print_program_info)
m_menu.add_separator()
m_menu.add_cascade(label='Author',command=print_author)

main_menu.add_cascade(label='Menu',menu=m_menu)
root.config(menu=main_menu,bg='#8ea8b2')


#Рабочая область
a = StringVar()
b = StringVar()
#
a_label = Label(text = " 2/10")
b_label = Label(text = " 10/2")
#
a_label.grid(row=0, column=2)
b_label.grid(row=2, column=2)
#
a_entry = Entry(textvariable=a)
b_entry = Entry(textvariable=b)
#
a_entry.grid(row=0, column=1, padx=5, pady=5)
b_entry.grid(row=2, column=1, padx=5, pady=5)


#кнопка Решить 2/10
message_button = Button(text="Решить 2/10", command=twte)
message_button.grid(row=0, column=6, padx=5, pady=5)

#кнопка Решить 10/2
message_button = Button(text="Решить 10/2", command=tetw)
message_button.grid(row=2, column=6, padx=5, pady=5)

#кнопка стереть
message_button = Button(text="С", command=delete)
message_button.grid(row=0, column=7, padx=5, pady=5)

# выключаем возможность изменять окно
root.resizable(width=False, height=False)

# запускаем главное окно
root.mainloop()
