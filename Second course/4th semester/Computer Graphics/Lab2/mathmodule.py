from math import sin, cos, pi, acos

def f(a,b,t):
    return [a*cos(t),b*sin(t),1]


def get_ellipse(a=3,b=1):
    points = []

    start = -pi/2
    end = pi/2
    step = 0.01

    while start < end + step/2:
        points.append(f(a,b,start))
        start += step
        
    return points


def ff(x,k,b):
    return [x,k*x+b,1]


def get_line(c=10,d=1):
    b = d
    k = b/c
    return [ff(-c,k,b),ff(0,k,b)]


def get_figure(a=3,b=1,c=10):
    return get_line(c,-b)+get_ellipse(a,b)+get_line(c,b)


def mul_matr_vec(matr,vec):
    res = [0,0,0]
    for i in range(3):
        tmp = 0
        for j in range(3):
            tmp += vec[j]*matr[j][i]
        res[i] = tmp

    return res


def move(arr,dx,dy):
    matr = [[1,0,0],[0,1,0],[dx,dy,1]]
    res = [] 
    for i in arr:
        res.append(mul_matr_vec(matr, i))

    return res


def turn(arr,xc,yc,angle):
    matr = [[cos(angle),-sin(angle),0],[sin(angle),cos(angle),0],[0,0,1]]
    res = []
    arr = move(arr,-xc,-yc)
    for i in arr:
        res.append(mul_matr_vec(matr, i))
    res = move(res,xc,yc)
    
    return res


def scale(arr,xc,yc,kx,ky):
    matr = [[kx,0,0],[0,ky,0],[0,0,1]]

    res = []
    arr = move(arr,-xc,-yc)
    for i in arr:
        res.append(mul_matr_vec(matr, i))
    res = move(res,xc,yc)
    
    return res


def f1(x,k,b):
    return k*x+b


def f2(x,a,b):
    c = acos(x/a)
    return b*sin(c)


def get_brush(a=3,b=1,c=10):
    res = []

    k1 = b/c
    k2 = -k1
    b1 = b
    b2 = -b1
    
    x1 = -c*0.98
    x2 = a
    h = b/4
    step = b/2
    while x1 < x2 + step/2:
        if x1 < -c/2:
            h = f1(x1,k1,b1)/2
        else:
            h = b/4
        tmp1 = x1-h
        tmp2 = x1+h
        if tmp2 >= a:
            x1 += step
            continue
        if tmp1 <= 0:
            y1 = f1(tmp1,k1,b1)
        else:
            y1 = f2(tmp1,a,b)
        if tmp2 <= 0:
            y2 = f1(tmp2,k2,b2)
        else:
            y2 = f2(tmp2,a,-b)
        res.append([tmp1, y1, 1])
        res.append([tmp2, y2, 1])
        x1 += step
        
    return res


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    a = get_figure()
    x = []
    y = []
    for i in a:
        x.append(i[0])
        y.append(i[1])
    plt.plot(x,y)

    a = scale(a,0,0,0.5,0.5)
    x1 = []
    y1 = []
    for i in a:
        x1.append(i[0])
        y1.append(i[1])
    plt.plot(x1,y1)

    a = turn(a,0,0,pi/2)
    x2 = []
    y2 = []
    for i in a:
        x2.append(i[0])
        y2.append(i[1])
    plt.plot(x2,y2)
    
    plt.show()
