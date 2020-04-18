# метод трапеций s = (f(x[i]) + f(x[i+1])/2*h

def f(x):
    return x


def integral(a, b, n, f):
    total = 0
    h = (b-a)/n
    for i in range(n):
        total += (f(a) + f(a + h))
        a += h
    total *= h/2
    return total


a, b = map(float, input('Введите границы интегрирования: ').split())
n = int(input('Введите количество участков разбиения для интегрирования: '))

I = integral(a, b, n, f)
print('Интеграл равен: {:.4f}'.format(I))
print(I)
    
