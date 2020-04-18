from PyQt5.QtCore import Qt
from plot import plot_all
from math import sqrt, pi, cos, sin

def middle_dot_circle(bg,xc,yc,R,size):
    p = int(1 -R)
    x = 0
    y = R

    plot_all(bg,x,y,xc,yc,size)
    plot_all(bg,y,x,xc,yc,size)
    
    while (x < y):
        x += 1
        if (p < 0):
            p += 2*x + 1
        else:
            y -= 1
            p += 2*(x-y) + 1

        plot_all(bg,x,y,xc,yc,size)
        plot_all(bg,y,x,xc,yc,size)


def canon_circle(bg,xc,yc,R,size):
    r2 = R*R
    x_max = round(R/sqrt(2))

    x = 0
    while x <= x_max:
        y = round(sqrt(r2 - x*x))
        plot_all(bg,x,y,xc,yc,size)
        x += 1

    y = round(sqrt(r2 - x_max*x_max))
    while y >= 0:
        x = round(sqrt(r2 - y*y))
        plot_all(bg,x,y,xc,yc,size)
        y -= 1


def param_cicrle(bg,xc,yc,R,size):
    dt = 1 / R
    m = pi/2*1.1
    alpha = 0
    while alpha <= m:
        x = round(R * cos(alpha))
        y = round(R * sin(alpha))
        plot_all(bg,x,y,xc,yc,size)
        alpha += dt


def bresenham_circle(bg,xc,yc,R,size):
    x = 0
    y = R

    err = 2*(1 - R)
    err1 = 0
    err2 = 0

    while (y >= 0):
        plot_all(bg,x,y,xc,yc,size)
        if err < 0:
            err1 = 2*err + 2*y - 1
            if err1 <= 0:
                x += 1
                err += 2*x + 1
            else:
                x += 1
                y -= 1
                err += 2*(x-y+1)
        elif err > 0:
            err2 = 2*err - 2*x - 1
            if err2 <= 0:
                x += 1
                y -= 1
                err += 2*(x-y+1)
            else:
                y -= 1
                err += -2*y + 1
        else:
            x += 1
            y -= 1
            err += 2*(x-y+1)

    
