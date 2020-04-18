#               Гасанзаде Мухаммедали Алиназим оглы
import math as m
x1,y1 = map(float,input('Введите координаты точки A:').split(' '))
x2,y2 = map(float,input('Введите координаты точки B:').split(' '))
x3,y3 = map(float,input('Введите координаты точки C:').split(' ')) 

#Нахождение длины сторон a,b,c
a = m.sqrt(abs(x2-x1)**2+abs(y2-y1)**2)
b = m.sqrt(abs(x3-x2)**2+abs(y3-y2)**2)
c = m.sqrt(abs(x3-x1)**2+abs(y3-y1)**2)

if (x1 == x2 and x2 == x3) or (y1 == y2 and y2 == y3) or (x1 == 0 and y1 == 0 and x2 > 0 and x3 > 0 and y2 > 0 and y3 > 0 and x2 / y2 == x3 / y3) or (x2 == 0 and y2 == 0 and x1 > 0 and x3 > 0 and y1 > 0 and y3 > 0 and  x1 / y1 == x3 / y3)\
   or (x3 == 0 and y3 == 0 and x1 > 0 and x2 > 0 and y1 > 0 and y2 > 0 and  x2 / y2 == x1 / y1) or (x1 > 0 and x2 > 0 and x3 > 0 and y1 > 0 and y2 > 0 and y3 > 0 and x1 / y1 == x2 / y2 and x2 / y2 == x3 / y3):
    print('Это не треугольник пока')
else:
    #Нахождение площади треугольника
    cs = (a**2+c**2-b**2)/(2*a*c)
    SQ = a*c*m.sqrt(1-cs**2)/2
    print(SQ)
