import time
import random
from time import perf_counter


                # Стандартный алгоритм умножения матриц
def ord_matr_mul(a, b, c):
    m = len(a)
    q = len(b[0])
    n = len(b)

    for i in range(m):
        for j in range(q):
            for k in range(n):
                c[i][j] = c[i][j] + a[i][k] * b[k][j]

    return c
    
                            # Алгоритм Винограда
def vin_matr_mul(a, b, c):
    m = len(a)
    q = len(b[0])
    n = len(b)
    MulH = [0] * m
    MulV = [0] * q

    for i in range(m):
        for j in range(0, n - 1, 2):
            MulH[i] -= a[i][j] * a[i][j + 1]
            
    for i in range(q):
        for j in range(0, n - 1, 2):
            MulV[i] -= b[j][i] * b[j + 1][i]

    for i in range(m):
        for j in range(q):
            c[i][j] = MulH[i] + MulV[j]
            for k in range(0, n - 1, 2):
                c[i][j] += (a[i][k] + b[k + 1][j]) * (a[i][k + 1] + b[k][j])

    if n % 2:
        for i in range(m):
            for j in range(q):
                c[i][j] += a[i][n - 1] * b[n - 1][j]

    return c

                # Алгоритм Винограда с набором оптимизаций
def opt_vin_matr_mul(a, b, c):
    m = len(a)
    q = len(b[0])
    n = len(b)
    MulH = [0] * m
    MulV = [0] * q

    n1 = n - 1

    for i in range(m):
        for j in range(0, n1, 2):
            MulH[i] -= a[i][j] * a[i][j + 1]
            
    for i in range(q):
        for j in range(0, n1, 2):
            MulV[i] -= b[j][i] * b[j + 1][i]

    if n % 2:
        for i in range(m):
            for j in range(q):
                buf = MulH[i] + MulV[j] + a[i][n1] * b[n1][j]
                for k in range(0, n1, 2):
                    buf += (a[i][k] + b[k + 1][j]) * (a[i][k + 1] + b[k][j])
                c[i][j] = buf
    else:
        for i in range(m):
            for j in range(q):
                buf = MulH[i] + MulV[j]
                for k in range(0, n1, 2):
                    buf += (a[i][k] + b[k + 1][j]) * (a[i][k + 1] + b[k][j])
                c[i][j] = buf

    return c

def get_random_matrix(n):
    matrix = []
    
    for i in range(n):
        matrix.append([])
        for j in range(n):
            matrix[i].append(random.randint(0, 10000))

    return matrix

def get_zero_matrix(n, m = -1):
    if m == -1:
        m = n
    
    matrix = []
    
    for i in range(n):
        matrix.append([])
        for j in range(m):
            matrix[i].append(0)

    return matrix

def input_matrix(str):
    print(str)
    m,n = map(int,input().split(' '))
    A = []
    
    for i in range(m):
        A.append(list(map(int,input().split(' '))))

    return A

def print_matrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])

    return matrix

def get_calc_time(func, matr1, matr2, matr3, it):
    t1_start = perf_counter()

    for i in range(it):        
        func(matr1, matr2, matr3)
        t1_stop = perf_counter()

    return (t1_start/it)
