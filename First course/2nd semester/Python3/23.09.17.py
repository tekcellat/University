import math as m
x1,y1 = map(float,input('Введите координаты точки A:').split(','))
x2,y2 = map(float,input('Введите координаты точки B:').split(','))
x3,y3 = map(float,input('Введите координаты точки C:').split(','))
x4,y4 = map(float,input('Введите координати точки D:').split(','))

# длина сторон
a = m.sqrt(abs(x2-x1)**2+abs(y2-y1)**2)
b = m.sqrt(abs(x3-x2)**2+abs(y3-y2)**2)
c = m.sqrt(abs(x3-x1)**2+abs(y3-y1)**2)
d = m.sqrt(abs(x4-x1)**2+abs(y4-y1)**2)
e = m.sqrt(abs(x3-x4)**2+abs(y3-y4)**2)
f = m.sqrt(abs(x4-x2)**2+abs(y4-y2)**2)
k = m.degrees(m.acos((b**2+c**2-a**2)/(2*b*c)))
l = m.degrees(m.acos((a**2+c**2-b**2)/(2*a*c)))
n = m.degrees(m.acos((a**2+b**2-c**2)/(2*a*b)))
if a < b and a < c :
    d = (1/2)*m.sqrt(2*(b**2)+2*(c**2)-a**2)
    print('AB=', a)
    print('BC=', b)
    print('AC=', c)
    print('M=', d)
else:
   if b < a and b < c :
       d = (1/2)*m.sqrt(2*(a**2)+2*(c**2)-b**2)
       print('AB=', a)
       print('BC=', b)
       print('AC=', c)
       print('M=', d)
   else:
     if c < a and c < b :
        d = (1/2)*m.sqrt(2*(a**2)+2*(b**2)-c**2)  
        print('AB=', a)
        print('BC=', b)
        print('AC=', c)
        print('M=', d)
S=k+l+n
if S == 180
    
