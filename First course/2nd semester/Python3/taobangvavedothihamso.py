""" b1 = pow(exp,-t) - pow(t-1,2)
    b2 = 4.07*t**4 + 12.7*t**3 + 8.7*t**2 + 10.8*t + 18.8
    t = -2.6(0.1)0
    use for loop
    subtration max and min b1
"""
import math as m

def my_range(start, stop, step):
    while start < stop:
        yield start
        start += step
a = []

print("---------------------------------------------------")
print("|       T        |       B1       |       B2      |")
print("---------------------------------------------------")
for t in my_range(-2.6,0.1,0.1): 
    b1 = m.exp(-t) - (t-1)**2
    b2 = 4.07* t**4 + 12.7* t**3 + 8.7* t**2 + 10.8*t + 18.8
    
    print("|{:9.1f}".format( t),end = "       |  ")
    print("{:8.2f}".format( b1),end = "      |  ")
    print("{:8.2f}".format( b2),end = "     |  ")
    print()
    a.append(b1)
    
print("---------------------------------------------------")
print()

min = min(a)
max = max(a)
b = max - min
print("max - min = ",b)

print("      min                                                                                                     max")
print("      ---------------------------------------------------------------------------------------------------------->")
for t in my_range(-2.6,0,0.1):
    b1 = m.exp(-t) - (t - 1) ** 2
    b2 = m.exp(-0) - (0 - 1) ** 2
    f = (b1 - min)/(max - min)
    c = int(f//0.01)
    d = int(((0 - min)/(max - min))//0.01)
    if b1 > 0:
        print(round(t, 1)," "*(d+3),"|"," "*(c - d),"*")    
    elif b1 < 0:
        print(round(t, 1)," "*(c),"*"," "*(d - c),"|")
print(round(0.00, 1)," "*(d+4),"*")
print("       "," "*d,"|OX")



