def f(x):
    return x*x

a = input('Введите нижний предел инт. : ')
b = input('Введите верхний предел инт. : ')
n = int(input("Введите количество разбиений n: "))

def middlerect(f,a,b,n):
    s = 0
    h = (b-a)/n
    for i in range(n):
        s += f(a+i*h+h/2)
    s *= h
    return s

#print(middleRect(f,a,b,n))
print('{:<13}'.format("сред тр"),'{:<15.8f}'.format(middlerect(f,a,b,n)))
