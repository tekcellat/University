from PyQt5.QtCore import Qt

# Draw one point in correct size
def plot(bg,x,y,size):
    if size == 1:
        bg.drawPoint(x,y)
    else:
        bg.drawRect(x*size,y*size,size,size)


def plot_all(bg,x,y,xc,yc,size):
    plot(bg,xc+x,yc+y,size)
    plot(bg,xc-x,yc+y,size)
    plot(bg,xc+x,yc-y,size)
    plot(bg,xc-x,yc-y,size)


def find_dx(x1,x2,size=1):
    if x2 - x1 > 0:
        return size
    elif x2 - x1 < 0:
        return -size
    else:
        return 0


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def floor(x):
    return abs(x) - abs(int(x))


def fpart(x):
    if x < 0:
        return 1 - (x - floor(x))
    
    return 1 - floor(x)

def rfpart(x):
    return 1 - fpart(x)
