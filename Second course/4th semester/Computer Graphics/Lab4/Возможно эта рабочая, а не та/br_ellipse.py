from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from plot import *
from math import pi, sqrt, cos, sin, acos

def middle_dot_ellipse(bg,xc,yc,a,b,size):
    x = 0
    y = b

    b2 = b*b
    a2 = a*a
    ad = a2*2
    bd = b2*2

    x_max = a2/sqrt(a2+b2)
    teta = -ad*y
    dx = 0

    fpr = b2 - a2*y + a2*0.25
    
    while x <= x_max:
        plot_all(bg,x,y,xc,yc,size)
        
        if fpr > 0:
            y -= 1
            teta += ad
            fpr += teta

        dx += bd
        x += 1
        fpr += dx + b2

    # Part 2
    fpr += 0.75*(a2 - b2) - (b2*x + a2*y)

    teta = bd*x
    dy = -ad*y
    
    while y >= 0:
        plot_all(bg,x,y,xc,yc,size)
        
        if fpr < 0:
            x += 1
            teta += bd
            fpr += teta

        dy += ad
        fpr += dy + a2
        y -= 1


def canon_ellipse(bg,xc,yc,a,b,size):
    a2 = a*a
    b2 = b*b

    c1 = b/a
    c2 = a/b
    x_max = round(a2/sqrt(a2+b2))
    
    x = 0
    while x <= x_max:
        y = round(c1 * sqrt(a2 - x*x))
        plot_all(bg,x,y,xc,yc,size)
        x += 1

    y = round(c1 * sqrt(a2 - x_max*x_max))
    while y >= 0:
        x = round(c2 * sqrt(b2 - y*y))
        plot_all(bg,x,y,xc,yc,size)
        y -= 1


def param_ellipse(bg,xc,yc,a,b,size):
    alpha = pi/2
    dx = 1/a
    dy = 1/b
    
    a2 = a*a
    b2 = b*b

    t_x_max = acos(a2/(a2+b2))

    while alpha >= t_x_max:
        x = round(a * cos(alpha))
        y = round(b * sin(alpha))
        plot_all(bg,x,y,xc,yc,size)
        alpha -= dx

    alpha = t_x_max
    while alpha >= -1:
        x = round(a * cos(alpha))
        y = round(b * sin(alpha))
        plot_all(bg,x,y,xc,yc,size)
        alpha -= dy
    

def bresenham_ellipse(bg,xc,yc,a,b,size):
    a2 = a*a
    b2 = b*b
    ad = 2 * a2
    bd = 2 * b2

    x = 0
    y = b
    
    err = a2 + b2 - ad * y
    err1 = 0
    err2 = 0

    while (y >= 0):
        plot_all(bg,x,y,xc,yc,size)
        if (err < 0):
            err1 = 2*err + ad*y - a2
            
            if (err1 < 0):
                x += 1
                err += bd*x +b2
            else:
                y -= 1
                x += 1
                err += bd*x + b2 + a2 - ad*y
        elif err > 0:
            err2 = 2*err - bd*x - b2
            if (err2 <= 0):
                y -= 1
                x += 1
                err += bd*x + b2 + a2 - ad*y
            else:
                y -= 1
                err += a2 - ad*y
        else:
            y -= 1
            x += 1
            err += bd*x + b2 + a2 - ad*y
