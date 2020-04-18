#No comment
import math as m
w,p,k = map(float,input('Введите (Нач. коорд)w (Конеч. коорд)p (Шаг)k: ').split( ))
def my_range(w, p, k):
    while w < p:
        yield w
        w += k
a = []

print("---------------------------------------------------")
print("|       T        |       A       |       B        |")
print("---------------------------------------------------")
for i in my_range(w,p,k): 
    v1 = m.exp(-i) - (i-1)**2
    v2 = 5.07* i**3 + 10.5* i**3 + 8.7* i**2 + 6.8*i + 18.8
    
    print("|{:9.1f}".format( i),end = "       |  ")
    print("{:8.2f}".format( v1),end = "      |  ")
    print("{:8.5f}".format( v2),end = "     |  ")
    print()
    a.append(v1)
    
print("---------------------------------------------------")
print()

min = min(a)
max = max(a)
v = max - min
print("max - min = ",v)

print("      min                                                                                                     max")
print("      ---------------------------------------------------------------------------------------------------------->")
for i in my_range(w,p,k):
    v1 = m.exp(-i) - (i - 1) ** 2
    v2 = m.exp(-0) - (0 - 1) ** 2
    f = (v1 - min)/(max - min)
    c = int(f//0.01)
    d = int(((0 - min)/(max - min))//0.01)
    if v1 > 0:
        print(round(i, 1)," "*(d+3),"|"," "*(c - d),"*")    
    elif v1 < 0:
        print(round(i, 1)," "*(c),"*"," "*(d - c),"|")
print(round(0.00, 1)," "*(d+4),"*")



