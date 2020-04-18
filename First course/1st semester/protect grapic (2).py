a,b,h = map(float,input('Введите (Нач. коорд)w (Конеч. коорд)p (Шаг)k: ').split( ))
def my_range(a,b,h):
    while a < b:
        yield a
        a += h
L = []

print("----------------------------------")
print("|       T        |       A       |")
print("----------------------------------")
for i in my_range(a,b,h): 
    v1 = i**2 - 49
    
    print("|{:9.1f}".format( i),end = "       |  ")
    print("{:8.2f}".format( v1),end = "      |  ")
    print()
    L.append(v1)
    
print("----------------------------------")
print()

min = min(L)
max = max(L)

print("      min                                                                                                     max")
print("      ---------------------------------------------------------------------------------------------------------->")
for i in my_range(a,b,h):
    v1 = (-i)**2 - 49
    f = (v1 - min)/(max - min)
    c = int(f//0.01)
    d = int(((0 - min)/(max - min))//0.01)
    if v1 > 0:
        print(round(i, 1)," "*(d+3),"|"," "*(c - d),"*")    
    elif v1 < 0:
        print(round(i, 1)," "*(c),"*"," "*(d - c),"|")
print(round(0.00, 1)," "*(d+4),"*")



