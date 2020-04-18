from tkinter import *
from tkinter import messagebox
from mathmodule import *
from math import pi

CANV_START_WIDTH = 800
CANV_START_HEIGHT = 800
A = 30
B = 50
C = 300
OX = CANV_START_WIDTH/2
OY = CANV_START_HEIGHT/2
AXIS = True
INFRONT = False
# Stack of operations
OP_ST = []

# Main window
root = Tk()
root.title("Возможно здесь должен быть заголовок")
root.geometry('220x480+810+0')
root.resizable(False, False)

# Buttons frame
Buttons = Frame(root)

top = Toplevel()
top.geometry('800x800+0+0')
top.resizable(False, False)
# Canvas
Canv = Canvas(top, bg = 'White',
              width = CANV_START_WIDTH, height = CANV_START_HEIGHT)

# Frames
Move = Frame(Buttons)
Turn = Frame(Buttons)
Scale = Frame(Buttons)

# Labels
# Move
Mname = Label(Move, text = "Перенос:",
              font = "Arial 14").grid(row = 0, column = 0, columnspan = 4)
MxL = Label(Move, text = "dX:",
            font = "Arial 14").grid(row = 1, column = 0)
MyL = Label(Move, text = "dY:",
            font = "Arial 14").grid(row = 1, column = 2)
# Scale
Sname = Label(Scale, text = "Масштабирование:",
              font = "Arial 14").grid(row = 0, column = 0, columnspan = 4)
SxL = Label(Scale, text = "Kx:",
            font = "Arial 14").grid(row = 1, column = 0)
SyL = Label(Scale, text = "Ky:",
            font = "Arial 14").grid(row = 1, column = 2)
ScxL = Label(Scale, text = "Xc:",
             font = "Arial 14").grid(row = 2, column = 0)
ScyL = Label(Scale, text = "Yc:",
             font = "Arial 14").grid(row = 2, column = 2)
# Turn
TangL = Label(Turn, text = "Угол:",
              font = "Arial 14").grid(row = 2, column = 0, columnspan = 2)
TyL = Label(Turn, text = "Yc:",
            font = "Arial 14").grid(row = 1, column = 2)
Tname = Label(Turn, text = "Поворот:",
              font = "Arial 14").grid(row = 0,column = 0, columnspan = 4)
TxL = Label(Turn, text = "Xc:",
            font = "Arial 14").grid(row = 1, column = 0)

# Entries
# Move
MxV = Entry(Move, bd = 5, width = 5)
MyV = Entry(Move, bd = 5, width = 5)
# Scale
SyV = Entry(Scale, bd = 5, width = 5)
ScxV = Entry(Scale, bd = 5, width = 5)
ScyV = Entry(Scale, bd = 5, width = 5)
SxV = Entry(Scale, bd = 5, width = 5)
# Turn
TxV = Entry(Turn, bd = 5, width = 5)
TyV = Entry(Turn, bd = 5, width = 5)
TangV = Entry(Turn, bd = 5, width = 10)

# Packing entries
# Move
MxV.grid(row = 1, column = 1)
MyV.grid(row = 1, column = 3)
# Scale
SxV.grid(row = 1, column = 1)
SyV.grid(row = 1, column = 3)
ScyV.grid(row = 2, column = 3)
ScxV.grid(row = 2, column = 1)
# Turn
TangV.grid(row = 2, column = 2, columnspan = 2)
TxV.grid(row = 1, column = 1)
TyV.grid(row = 1, column = 3)

# Points and brush
Points = []
Brush = []

def make_turn(ev=None):
    global TxV, TyV, TangV
    global Points
    global Canv
    global Brush
    
    Tcode = 0
    
    Tx = TxV.get()
    try:
        Tx = float(Tx)
        Ty = float(TyV.get())
    except ValueError:
        messagebox.showinfo("Warning", "Неверно заданы "+
                            "коэфициенты поворота!")
        Tcode = 1
        #return
        
    try:
        Tang = float(TangV.get())
    except ValueError:
        messagebox.showinfo("Warning", "Неверно задан "+
                            "угол поворота!")
        Tcode = 1
        #return
    
    flag = len(OP_ST) >= 1
    if Tcode == 0 and flag:
        Points = turn(Points,Tx,Ty,(Tang/180)*pi)
        Brush = turn(Brush,Tx,Ty,(Tang/180)*pi)
        OP_ST.append([Points,Brush])
        draw()
    

def make_scale(ev=None):
    global ScyV, ScxV, SxV, SyV
    global Points
    global Canv
    global Brush
    
    Scode = 0
    try:
        Scx = float(ScxV.get())
        Scy = float(ScyV.get())
    except ValueError:
        messagebox.showinfo("Warning", "Неверно заданы "+
                            "коэфициенты масштабирования!")
        Scode = 1
        #return

    try:
        Sx = float(SxV.get())
        Sy = float(SyV.get())
    except ValueError:
        messagebox.showinfo("Warning", "Неверно задан "+
                            "центр масштабирования!")
        Scode = 1
        #return

    flag = len(OP_ST) >= 1
    if Scode == 0 and flag:
        Points = scale(Points,Scx,Scy,Sx,Sy)
        Brush = scale(Brush,Scx,Scy,Sx,Sy)
        OP_ST.append([Points,Brush])
        draw()


def make_move(ev=None):
    global MxV, MyV
    global Points
    global Canv
    global Brush
    
    Mcode = 0
    
    try:
        Mx = float(MxV.get())
        My = float(MyV.get())
    except ValueError:
        messagebox.showinfo("Warning", "Неверно задан "+
                            "коэффициенты перемещения!")
        Mcode = 1
        #return

    flag = len(OP_ST) >= 1
    if Mcode == 0 and flag:
        Points = move(Points,Mx,My)
        Brush = move(Brush,Mx,My)
        OP_ST.append([Points,Brush])
        draw()


def show_axis(ev=None):
    global OX
    global OY
    global Canv

    Canv.create_line([OX,0],[OX,CANV_START_HEIGHT],arrow=LAST,fill='gray')
    Canv.create_text(OX+20,CANV_START_HEIGHT,text="Y",
          font="Verdana 20",anchor="s",justify=LEFT)
    Canv.create_line([0,OY],[CANV_START_WIDTH,OY],arrow=LAST,fill='gray')
    Canv.create_text(CANV_START_WIDTH-10,OY+30,text="X",
          font="Verdana 20",anchor="s",justify=LEFT)


def draw(ev=None):
    global Points
    global Canv
    global AXIS
    global INFRONT
    global Brush

    if len(Points) == 0:
        Points = get_figure(A,B,C)
        Brush = get_brush(A,B,C)
        OP_ST.append([Points,Brush])

    Canv.delete('all')
    points = []
    for i in Points:
        points.append([i[0]+OX,
                       i[1]+OY])

    if AXIS and not INFRONT:
        show_axis()
    Canv.create_polygon(points, fill = 'white', outline = 'black')

    if AXIS and INFRONT:
        show_axis()
    
    brush = []
    for i in range(1,len(Brush),2):
        brush.append([Brush[i-1][0]+OX,Brush[i-1][1]+OY,
                      Brush[i][0]+OX,Brush[i][1]+OY])
        
    for i in brush:
        Canv.create_line(i)


def cancel(ev=None):
    global Points
    global Canv
    global OP_ST
    global Brush
    
    if len(OP_ST) > 1:
        Points = OP_ST[len(OP_ST)-2][0]
        Brush = OP_ST[len(OP_ST)-2][1]
        OP_ST = OP_ST[:-1]
        draw()
    else:
        Points = []
        Canv.delete('all')


def reset(ev=None):
    global Points
    global OP_ST
    global Brush

    draw()

    Points = OP_ST[0][0]
    Brush = OP_ST[0][1]
    OP_ST = OP_ST[0:]

    draw()
    

def switch_axis(ev=None):
    global AXIS
    AXIS = not AXIS
    if Points != []:
        draw()
    else:
        if AXIS:
            show_axis()
        else:
            Canv.delete('all')


def front(ev=None):
    global INFRONT
    INFRONT = not INFRONT
    if Points != []:
        draw()
    
draw()

DrawButton = Button(Buttons, text = "Draw",
                    font = "Verdana 14",command = draw, width = 8)
ResetButton = Button(Buttons, text = "Reset",
                     font = "Verdana 14", command = reset, width = 8)
AxisButton = Button(Buttons, text = "Hide/Show axis",
                     font = "Verdana 14", command = switch_axis, width = 16)
FrontButton = Button(Buttons, text = "Axis on top",
                     font = "Verdana 14", command = front, width = 16)
CancelButton = Button(Buttons, text = "Cancel",
                    font = "Verdana 14", command = cancel, width = 8)
MoveButton = Button(Buttons, text = "Move",
                    font = "Verdana 14",command = make_move, width = 8)
ScaleButton = Button(Buttons, text = "Scale",
                    font = "Verdana 14",command = make_scale, width = 8)
TurnButton = Button(Buttons, text = "Turn",
                    font = "Verdana 14",command = make_turn, width = 8)

ResetButton.grid(row = 6, column = 0)
AxisButton.grid(row = 7, column = 0, columnspan = 2)
FrontButton.grid(row = 8, column = 0, columnspan = 2)
CancelButton.grid(row = 6, column = 1)
Turn.grid(row = 4, column = 0, columnspan = 2)
TurnButton.grid(row = 5, column = 0, columnspan = 2)
Scale.grid(row = 2, column = 0, columnspan = 2)
ScaleButton.grid(row = 3, column = 0, columnspan = 2)
Move.grid(row = 0, column = 0, columnspan = 2)
MoveButton.grid(row = 1, column = 0, columnspan = 2)

Buttons.pack(side = TOP, fill = BOTH)
Canv.pack(side = TOP, fill = BOTH)

top.mainloop()
root.mainloop()
