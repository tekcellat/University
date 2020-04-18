def f(x): 
    return x*x


def trapeze(f,a,b,n): 
    s = (f(a)+f(b))/2
    h = (b-a)/n
    for i in range(1,n):
        s += f(a+i*h)
    s *= h
    return s

 
a = float(input("Введите нижний предел интегрирования: "))
b = float(input("Введите верхний предел интегрирования: "))
n1 = int(input("Введите количество разбиений n: "))
eps = float(input("Введите точность: "))


n = 1
i = 0
while True:
    i += 1
    k = abs(trapeze(f,a,b,2*n) - trapeze(f,a,b,n))
    if abs(k) < eps:
        break
    else:
        n = 2*n
print(n)


print('{:<13}'.format("Трапеция"),'{:<15.8f}'.format(trapeze(f,a,b,n1)))
    
