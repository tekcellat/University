a = float(input("Введите начало интервала: "))
b = float(input("Введите конец интервала: "))
N = int(input("Введите количество отрезков: "))

if not N%2:
    def f(x):
        return 3 * x**2 + 6
    h = (b-a)/2/N
    S = f(a) + f(b)
    for i in range(1,2*N):
        if i%2:
            S += 4*f(a+h*i)
        else:
            S += 2*f(a+h*i)
    S *= h/3
    print("Результат: {:0.3f}".format(S))
else:
    print("N должно быть кратно 2")
