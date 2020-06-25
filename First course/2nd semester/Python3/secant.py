from math import sin

def f(x):
    return sin(x)

def root_search(a,b,eps,n):
    if f(a) == 0:
        return a,1,0
    if f(b) == 0:
        return b,1,0
    
    # 1-я итерация
    x1 = a
    x2 = b
    i = 1
    
    while (i <= n):
        y1 = f(x1)
        y2 = f(x2)
        if abs(y1 - y2) == 0:
            return '-', i, 2
        
        x = x1 - y1*(x1 - x2)/(y1 - y2)
        if abs(x - x1) < eps:
            return x, i, 0

        #переход к следующей итерации
        x2 = x1
        x1 = x
        i += 1

    return '-', i, 1

def finding(a,b,h,eps):    
    roots = []  # список корней
    res = []    # список интервалов
    kol = 0     # количество итераций
    aa = a      # начало отрезка
    bb = a      # конец отрезка

    #нахождение интервалов
    while bb < b:
        bb += h
        if bb > b:
            bb = b
        if f(aa)*f(bb)<=0:
            kol += 1
            res.append([aa,bb])
        aa += h

    #нахождение корней
    i = 0
    while len(res) > i:
        #список с информацией о корне
        rootX = root_search(res[i][0],res[i][1],eps,n)
        if (len(roots) == 0 or rootX[0] == '-' or
            roots[-1][0] == '-' or abs(rootX[0] - roots[-1][0]) > 1e-20):
            roots.append(rootX)
        else:
            res.pop(i)
            i -= 1
        i += 1
    return roots, res

a = float(input("Введите a: "))
b = float(input("Введите b: "))
h = float(input("Введите шаг: "))
eps = float(input("Введите точность: "))
n = int(input("Введите кол-во итераций: "))

roots,res = finding(a,b,h,eps)

print()
if len(roots) == 0 and len(res) == 0:
    print("Нет решений на данном интервале!")
else:
    print('  #',3*' '+'Интервал'+4*' ',
          4*' '+'X'+4*' ',3*' '+'F(x)'+3*' ',
          'Итерации','Код ошибки', sep = '\u2502')
    print(3*'\u2500',15*'\u2500',9*'\u2500',10*'\u2500',8*'\u2500',
          10*'\u2500', sep = '\u253c')
    for i in range(len(roots)):
        a1 = res[i][0]
        b1 = res[i][1]
        print("{:3d}".format(i+1),
              "{:7.3f};{:7.3f}".format(a1,b1),
              sep = '\u2502', end = '\u2502')
        
        if roots[i][0] != '-':
            print("{:9.4f}".format(roots[i][0]),
                  "{:10.3e}".format(f(roots[i][0])),
                  sep = '\u2502', end = '\u2502')
        else:
            print(9*'-', 10*'-', sep = '\u2502', end = '\u2502')
            
        print("{:8d}".format(roots[i][1]), roots[i][2], sep = '\u2502')
        
    print("\nКоды ошибок:")
    print("0 - нет ошибок")
    print("1 - большое количество итераций")
    print("2 - деление на 0")
