# Турысов

# Найти все корни уровнения f(x) = 0 с помощью метода Ньютона уточнения корней 
# Отрисовать график, отметить корни, экстремумы, точки перегиба


import matplotlib.pyplot as m
import numpy as num
from math import sin, cos

def f(x):
    return sin(x)*cos(x)

#f1 - производная f
def f1(x):
    return (f(x+eps) - f(x))/eps

#f2 - вторая производная f
def f2(x):
    return (f1(x+eps) - f1(x))/eps

#f3 - третья производная f
def f3(x):
    return (f2(x+eps) - f2(x))/eps

def pol_del(x0,x1, eps):
   i = 0
   while True:
       i+=1
       x2 = (x0 + x1)/2
       
       if (f(x1)*f(x2) < 0):
           x0 = x2
       else:
           x1 = x2
                 
       if abs(x1 - x0) < eps:
           return (x1+x0)/2, i

eps = float(input("Введите точность(0 для точности по умолчанию): "))
if eps == 0:
    eps = 0.001

h = float(input("Введите шаг: "))
a= -5
b = 5
xlist = num.linspace(a,b,1000) 
ylist = [f(x) for x in xlist] 
m.axis([a, b, -2, 2]) 
m.xlabel('x') 
m.ylabel('y') 
m.title('Function F(x)')
# Отрисовываем ось х
m.plot([a, b],[0.0, 0.0], color = 'k')
# Отрисовываем график функции f(x)
m.plot(xlist, ylist, label = u'f(x)', color = 'r')
m.grid(True)

print("-"*53)
print("|  N  |   Xn - Xn+1   |     x     |    f(x)   |  i  |")
print("-"*53)
# Номер корня
n = 1

flag_root = False

while a<b:
    # Проверяем, не пересекла ли функция ось х
    if f(a)*f(a+h)<=0:
        
        x, i = pol_del(a, a+h, eps)
        string = " {:.2f} - {:.2f} ".format(a, a+h)
        # Отмечаем корень на оси x
        if flag_root:
            m.scatter(x, 0.0, color = 'm')
        else:
            m.scatter(x, 0.0, label = u'f(x) = 0', color = 'm')
            flag_root = True
        
        print("|  {:d}  ".format(n),end = "|")
        print(string + " "*(15-len(string)), end = "|")
        if x < 0:
            print(" {:2.6f} ".format(x), end = "|")
        else:   
            print("  {:2.6f} ".format(x), end = "|")
        if f(x) < 0:
            print(" {:2.2e} ".format(f(x)), end = "|")
        else:
            print("  {:2.2e} ".format(f(x)), end = "|")
        print("  {:d}  |".format(i))

        n+=1

        
        
        
    a+=h
print("-"*53)

m.legend() 
m.show()





