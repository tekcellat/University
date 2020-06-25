import matplotlib.pyplot as m
import numpy as num
from math import sin, cos

def f(x):
    return x**2-1



def combine_method(x0,x1, eps):
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
a= float(input('Введите а: '))
b = float(input('Введите b: '))

print("-"*53)
print("|  N  |   Xn - Xn+1   |     x     |    f(x)   |  i  |")
print("-"*53)
# Номер корня
n = 1



while a<b:
        if (a+h) > b:
            h = b-a
        # Проверяем, не пересекла ли функция ось х
        if f(a)*f(a+h)<=0:
            x, i = combine_method(a, a+h, eps)   
            string = " {:.2f} - {:.2f} ".format(a, a+h)
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

