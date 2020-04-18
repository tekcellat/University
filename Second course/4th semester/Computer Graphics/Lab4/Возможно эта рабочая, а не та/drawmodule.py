from br_circle import *
from PyQt5.QtCore import Qt
from br_ellipse import *

def drawcircle(painter, circles, ellipses, draw_type):
    if draw_type == 0:
        for i in ellipses:
            painter.setPen(i[4])
            painter.setBrush(i[4])
            if i[6] == 0:
                middle_dot_ellipse(painter,i[0],i[1],i[2],i[3],i[5])
            elif i[6] == 1:
                bresenham_ellipse(painter,i[0],i[1],i[2],i[3],i[5])
            elif i[6] == 2:
                canon_ellipse(painter,i[0],i[1],i[2],i[3],i[5])
            elif i[6] == 3:
                param_ellipse(painter,i[0],i[1],i[2],i[3],i[5])
            elif i[6] == 4:
                std_ellipse(painter,i[0],i[1],i[2],i[3],i[5])
    else:
        for i in circles:
            painter.setPen(i[3])
            painter.setBrush(i[3])
            if i[5] == 0:
                middle_dot_circle(painter,i[0],i[1],i[2],i[4])
            elif i[5] == 1:
                bresenham_circle(painter,i[0],i[1],i[2],i[4])
            elif i[5] == 2:
                canon_circle(painter,i[0],i[1],i[2],i[4])
            elif i[5] == 3:
                param_cicrle(painter,i[0],i[1],i[2],i[4])
            elif i[5] == 4:
                std_circle(painter,i[0],i[1],i[2],i[4])


def std_ellipse(bg,xc,yc,a,b,size):
    if size == -1:
        bg.setBrush(Qt.white)
        bg.drawEllipse(xc-a,yc-b,2*a,2*b)
    else:
        canon_ellipse(bg,xc,yc,a,b,size)


def std_circle(bg,xc,yc,R,size):
    if size == -1:
        bg.setBrush(Qt.white)
        bg.drawEllipse(xc-R,yc-R,2*R,2*R)
    else:
        canon_circle(bg,xc,yc,R,size)
