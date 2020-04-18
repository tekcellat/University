#Защита интегралов: Сред тр


a = float(input("Введите нижний предел интегрирования: "))
b = float(input("Введите верхний предел интегрирования: "))
n = int(input("Введите количество разбиений n1: "))

def f(x):
    return x


def leftRect(f,a,b,n):
    s = 0
    h = (b-a)/n
    for i in range(n):
        s += f(a+i*h)
    s *= h
    return s



    

print('{:<13}'.format("сред тр"),'{:<15.8f}'.format(leftRect(f,a,b,n)))
      
