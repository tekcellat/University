from tkinter import *
from tkinter import messagebox
import math
from random import randint


root = Tk()
root.title ("Возможно здесь должен быть заголовок")
root.geometry('1250x700')
canv = Canvas(bg='white')
canv.pack(fill = BOTH, expand = 1)
root.resizable(width=False, height=False)
def main():
    global point_list, k, used_colors, k_zoom
    k = 0 #Номер точки
    k_zoom = 1
    point_list = []
    used_colors = []		
    route()
    add_button()
    edit_button()
    delete_button()
    delete_all_button()
    find_triangle()

def route():
    canv.create_line(480, 700, 480, 0, width = 1, fill = 'blue', arrow = LAST)
    canv.create_line(0, 350, 960, 350, width = 1, fill = 'red', arrow = LAST)
    #Боковое меню
    canv.create_line(960, 0, 960, 700, width = 2)
    canv.create_line(960, 39, 1250, 39)
    canv.create_line(960, 99, 1250, 99)
    canv.create_line(960, 133, 1250, 133)
    #Текст к кнопкам
    canv.create_text(970, 22, text = 'x: ')
    canv.create_text(1045, 22, text = 'y: ')
    canv.create_text(973, 52, text = '№: ')
    canv.create_text(1045, 52, text = 'x: ')
    canv.create_text(1115, 52, text = 'y: ')
    canv.create_text(973, 114, text = "№: ")

def draw_points():
    global point_list, k_zoom
    for i in range (len(point_list)):
        x = k_zoom * point_list[i][0] + (1 - k_zoom) * 480
        y = k_zoom * point_list[i][1] + (1 - k_zoom) * 350
        canv.create_oval(x - 1, y - 1, x + 1, y + 1,  width = 2)
        canv.create_text(x + 50, y - 10, font = '5', text = (i, '(', (point_list[i][0] - 480) / 100, ',', (690 - point_list[i][1] - 340) / 100, ')'))

def points_change(x, y, flag_x, flag_y):
    global point_list
    x = -x
    x = math.fabs(x - 480)
    y = math.fabs(y - 350)
    if (flag_x == True):
        x = -x
    if (flag_y == True):
        y = -y
    return x, y

def triangle(x1, y1, x2, y2, x3, y3, color):
    global used_colors, k_zoom
    colors = ["black", "darkgreen", "lightskyblue", "gold", "brown", "darkblue"]
    if (len(used_colors) == 3):
        used_colors = []
    i = randint(0, 3)
    while i in used_colors:
        i = randint(0, 3)
    if (color != -1):
        i = color

    x1 = k_zoom * x1 + (1 - k_zoom) * 480
    y1 = k_zoom * y1 + (1 - k_zoom) * 350
    x2 = k_zoom * x2 + (1 - k_zoom) * 480
    y2 = k_zoom * y2 + (1 - k_zoom) * 350
    x3 = k_zoom * x3 + (1 - k_zoom) * 480
    y3 = k_zoom * y3 + (1 - k_zoom) * 350

    canv.create_line((x1, y1, x2, y2), fill = colors[i])
    canv.create_line((x2, y2, x3, y3), fill = colors[i])
    canv.create_line((x3, y3, x1, y1), fill = colors[i])
    used_colors.append(colors[i])
    return i
    
def add_button():
    #Кнопка добавление 
    global add_x, add_y
    add_x = Entry(root)
    add_x.pack()
    add_x.place(x = 980, y = 10, width = 50)
    
    add_y = Entry(root)
    add_y.pack()
    add_y.place(x = 1050, y = 10, width = 50)
    
    button_1 = Button(root,text=u"Добавить точку")
    button_1.pack()
    button_1.place(x = 1100, y = 10, width = 140)
    button_1.bind("<Button-1>", get_A)

def get_A(root):
    global add_x, add_y, point_list, k
    x = add_x.get()
    y = add_y.get()
    x = float(x)
    y = float(y)
    flag_x = False
    flag_y = False
    if (x <= -4.9):
        flag_x = True
    if (y >=  3.6):
        flag_y = True
    x *= 100
    y *= 100
    x, y = points_change(x, y, flag_x, flag_y)
    point_list.append([x,y, k])
    k += 1
    canv.delete("all")
    draw_points()
    route()
    find_triangle()

def edit_button():
    global edit_n, edit_x, edit_y
    
    edit_n = Entry(root)
    edit_n.pack()
    edit_n.place(x = 980, y = 40, width = 50)

    edit_x = Entry(root)
    edit_x.pack()
    edit_x.place(x = 1050, y = 40, width = 50)
    
    edit_y = Entry(root)
    edit_y.pack()
    edit_y.place(x = 1120, y = 40, width = 50)

    button_2 = Button(root,text=u"Изменить точку")
    button_2.pack()
    button_2.place(x = 1100, y = 67, width = 140)
    button_2.bind("<Button-1>", get_E)

def get_E(root):
    global edit_n, edit_x, edit_y, point_list, k
    n = edit_n.get()
    x = edit_x.get()
    y = edit_y.get()
    n = int(n)
    x = float(x)
    y = float(y)
    flag_x = False
    flag_y = False
    if (x <= -4.9):
        flag_x = True
    if (y >=  3.6):
        flag_y = True
    x *= 100
    y *= 100
    x, y = points_change(x, y, flag_x, flag_y)
    point_list[n][0] = x
    point_list[n][1] = y
    canv.delete("all")
    draw_points()
    route()
    find_triangle()

def delete_button():
    global delete_n
    delete_n = Entry()
    delete_n.pack()
    delete_n.place(x = 980, y = 103, width = 50)

    button_3 = Button(root, text = u"Удалить точку")
    button_3.pack()
    button_3.place(x = 1100, y = 103, width = 140)
    button_3.bind("<Button-1>", get_D)

def get_D(root):
    global delete_n, point_list, k
    n = delete_n.get()
    n = int(n)
    if (n >= k):
        messagebox.showinfo("Warning", "Такой точки не существует")
        return -1
    del point_list[n]
    for i in range(n, len(point_list)):
        point_list[i][2] -= 1
    k -= 1
    canv.delete("all")
    draw_points()
    route()
    find_triangle()

def delete_all_button():
    button_4 = Button(root, text = u"Удалить все точки")
    button_4.pack()
    button_4.place(x = 1100, y = 135, width = 140)
    button_4.bind("<Button-1>", get_DA)

def get_DA(root):
    global k, point_list
    point_list = []
    k = 0
    canv.delete("all")
    route()

def find_triangle():
    global k
    kol_vo = 0
    angle_m = 180
    flag = False
    add_flag = False
    needed_points = []
    for i in range(len(point_list)):
        x1 = point_list[i][0]
        y1 = point_list[i][1]
        n_1 = point_list[i][2]
        for j in range(len(point_list)):
            x2 = point_list[j][0]
            y2 = point_list[j][1]
            n_2 = point_list[j][2]
            for o in range(len(point_list)):
                x3 = point_list[o][0]
                y3 = point_list[o][1]
                n_3 = point_list[o][2]
                if i != j and i != o and j != o:
                    #Проверка на существование треугольника
                    a, b, c = find_sides(x1, y1, x2, y2, x3, y3)
                    if a + b > c and a + c > b and b + c > a:
                        angle, x2_g, y2_g, x_m_c, y_m_c, x_b_b, y_b_b = min_angle(x1, y1, x2, y2, x3, y3)               
                        if (angle < angle_m):
                            needed_points = []
                            s = array(a, b, c)
                            needed_points.append([angle, s, i, j, o])
                            angle_m = angle
                            k_zoom = zoom(x1, y1, x2, y2, x3, y3)
                            canv.delete("all")
                            draw_points()
                            route()
                            color = triangle(x1, y1, x2, y2, x3, y3, -1)
                            triangle(x2_g, y2_g, x_m_c, y_m_c, x_b_b, y_b_b, color)
                            flag = True
                        elif (angle == angle_m):
                            s = array(a, b, c)
                            add_flag = False
                            for y in range(len(needed_points)):
                                if (i == needed_points[y][2] and j == needed_points[y][3] and o == needed_points[y][4]) or (i == needed_points[y][4] and j == needed_points[y][3] and o == needed_points[y][2]):
                                    add_flag = True
                            if add_flag != True:
                                needed_points.append([angle, s, i, j, o])
                                color = triangle(x1, y1, x2, y2, x3, y3, -1)
                                triangle(x2_g, y2_g, x_m_c, y_m_c, x_b_b, y_b_b, color)     
    if (flag == False) and (len(point_list) >= 3):
        for i in range(len(point_list) - 1):
            canv.create_line(point_list[i][0], point_list[i][1], point_list[i + 1][0], point_list[i + 1][1])
        messagebox.showinfo("Warning", "Все варианты вырождены")
    elif (flag == True) and (len(point_list) >= 3):
        for i in range(len(needed_points)):
            angle = needed_points[i][0]
            s = needed_points[i][1]

            x1 = point_list[needed_points[i][2]][0]
            y1 = point_list[needed_points[i][2]][1]
            n_1 = point_list[needed_points[i][2]][2]

            x2 = point_list[needed_points[i][3]][0]
            y2 = point_list[needed_points[i][3]][1]
            n_2 = point_list[needed_points[i][3]][2]

            x3 = point_list[needed_points[i][4]][0]
            y3 = point_list[needed_points[i][4]][1]
            n_3 = point_list[needed_points[i][4]][2]

            printf(x1, y1, x2, y2, x3, y3, angle, s, n_1, n_2, n_3)
            kol_vo += 1
    print("Количество треугольников: ", kol_vo)
    print("+_______________________________________+")


def array(a, b, c):
    p = (a + b + c) / 2
    s = math.sqrt(p * (p - a) * (p - b) * (p - c))
    s = round(s, 3)
    return s

def find_sides(x1, y1, x2, y2, x3, y3):
    a = (math.sqrt(abs(pow((x2 - x1), 2) + pow((y2 - y1), 2)))) 
    b = (math.sqrt(abs(pow((x3 - x2), 2) + pow((y3 - y2), 2)))) 
    c = (math.sqrt(abs(pow((x1 - x3), 2) + pow((y1 - y3), 2))))
    return a, b, c

def min_angle(x1, y1, x2, y2, x3, y3):
    a, b, c = find_sides(x1, y1, x2, y2, x3, y3)

    #Находим координату медианы
    x_m_a = (x1 + x2) / 2
    y_m_a = (y1 + y2) / 2
    
    x_m_b = (x2 + x3) / 2
    y_m_b = (y2 + y3) / 2
    
    x_m_c = (x3 + x1) / 2
    y_m_c = (y3 + y1) / 2

    #Находим координату биссектрисы
    x_b_b = (x3 + (a / b) * x1) / (1 + (a / b))
    y_b_b = (y3 + (a / b) * y1) / (1 + (a / b))

    #Находим угол между биссектрисой и медианой
    angle = (((x2 - x_m_c) ** 2) + ((y2 - y_m_c) ** 2) + ((x2 - x_b_b) ** 2) + ((y2 - y_b_b) ** 2) - ((x_m_c - x_b_b) ** 2) - ((y_m_c - y_b_b) ** 2)) / (2 * math.sqrt(((x2 - x_m_c) ** 2) + ((y2 - y_m_c) ** 2)) * math.sqrt(((x2 - x_b_b) ** 2) + ((y2 - y_b_b) ** 2)))
    angle = math.acos(angle)
    angle = round(angle * (180 / math.pi), 2)

    return angle, x2, y2, x_m_c, y_m_c, x_b_b, y_b_b

def zoom(x1, y1, x2, y2, x3, y3):
    global k_zoom
    i = 0
    x1k = x1
    x2k = x2
    x3k = x3
    y1k = y1
    y2k = y2
    y3k = y3
    while (x1 < 30 or x1 > 930) or (x2 < 30 or x2 > 930) or (x3 < 30 or x3 > 930) or (y1 < 30 or y1 > 670) or (y2 < 30 or y2 > 670) or (y3 < 30 or y3 > 670):
        x1 = k_zoom * x1 + (1 - k_zoom) * 480
        y1 = k_zoom * y1 + (1 - k_zoom) * 350
        x2 = k_zoom * x2 + (1 - k_zoom) * 480
        y2 = k_zoom * y2 + (1 - k_zoom) * 350
        x3 = k_zoom * x3 + (1 - k_zoom) * 480
        y3 = k_zoom * y3 + (1 - k_zoom) * 350
        if (x1 > 30 and x1 < 930) and (x2 > 30 and x2 < 930) and (x3 > 30 and x3 < 930) and (y1 > 30 and y1 < 670) and (y2 > 30 and y2 < 670) and (y3 > 30 and y3 < 670):
            return k_zoom
        else:
            x1 = x1k
            x2 = x2k
            x3 = x3k
            y1 = y1k
            y2 = y2k
            y3 = y3k
            i += 0.005
            k_zoom = 1
            k_zoom -= i
            
            

def printf(x1, y1, x2, y2, x3, y3, angle, s, n_1, n_2, n_3):
    print('Треугольник состоящий из точек:', n_1, ',', n_2, ',', n_3, '\nx1: ', (x1 - 480) / 100, "\ny1: ", (690 - y1 - 340) / 100, "\nx2: ", (x2 - 480) / 100, "\ny2: ", (690 - y2 - 340) / 100, "\nx3: ", (x3 - 480) / 100, "\ny3: ", (690 - y3 - 340) / 100, "\nИмеет наименьший угол между биссектрисой и медианой: ", angle,"\nЕго площадь равняется: ", s)

if __name__ == '__main__':
    main()

root.mainloop()
