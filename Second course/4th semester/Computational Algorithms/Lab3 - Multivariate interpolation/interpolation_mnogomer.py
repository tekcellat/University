from math import *
from prettytable import PrettyTable

def func(x, y):
    return x * x + y * y

def main():
    mas_x = []; mas_y = []
    tmp_x = []; tmp_y = []; tmp_y2 = []
    tmp_x3 = []; tmp_y3 = []
    matrix = []
    
    beg = 0; end = 10
    N = abs(end - beg) - 1
    eps = 1e-5
    
    for i in range(beg, end):
        tmp_x.append(i)
        tmp_y.append(i)

    matrix = create_new_matrix(func, tmp_x, tmp_y)
    print_matrix(tmp_x, tmp_y, matrix)

    n_X = int(input("input n for X: "))
    n_Y = int(input("input n for Y: "))
    x = float(input("input x: "))
    y = float(input("input y: "))
    
    mas_x = create_new_x_y(x, n_X, N, tmp_x)
    mas_y = create_new_x_y(y, n_Y, N, tmp_y)
    matrix = create_new_matrix(func, mas_x, mas_y)

    new_x = []
    for i in range(len(mas_x)):
        new_x.append(interpolation(y, n_Y, mas_y, matrix[i]))
        
    answer = interpolation(x, n_X,  mas_x, new_x)
    print("\nF(x, y) = ", answer)
    
def print_matrix(tmp_x, tmp_y, matrix):
    print("|X|Y|", end = " ")
    for i in range(0, len(tmp_x)):
        print("{:5d}".format(tmp_x[i]), end = " ")
    print()
    for i in range(0, len(tmp_x)):
        print("{:3d}".format(tmp_x[i])," ", end = " ")
        for j in range(0, len(tmp_y)):
            print( "{:5d}".format(matrix[i][j]), end = " ")
        print()
    print()
        
def create_new_matrix(f, tmp_x, tmp_y):
    matrix = []
    for i in range(0, len(tmp_x)):
        matrix.append([])
        for j in range(0, len(tmp_y)):
            matrix[i].append(f(tmp_x[i], tmp_y[j]))
    return matrix

def create_new_x_y(x, n, N, tmp_x):
    mas_x = []
    if (x <= tmp_x[0]):
        for i in range(0, n + 1):
            mas_x.append(tmp_x[i])
    elif (x >= tmp_x[N]):
        for i in range(len(tmp_x) - (n + 1), len(tmp_x)):
            mas_x.append(tmp_x[i])
    else:
        back = 0; up = 0
        for i in range(1, N):
            if((tmp_x[i - 1] <= x) and (tmp_x[i] > x)):
                up = i; back = i - 1
                for k in range(0, n + 1):
                    if (k % 2 == 0):
                        if (up < len(tmp_x)):
                            mas_x.append(tmp_x[up])
                            up += 1
                        elif (back >= 0):
                            mas_x.insert(0, tmp_x[back])
                            back -= 1
                    else:
                        if (back >= 0):
                            mas_x.insert(0, tmp_x[back])
                            back -= 1
                        elif(up < len(tmp_x)):
                            mas_x.append(tmp_x[up])
                            up += 1
    return mas_x

def interpolation(x, n, mas_x, mas_y):
    matrix = []
    matrix.append([])
    for i in range(0, n):
        matrix[0].append((mas_y[i] - mas_y[i + 1])/(mas_x[i] - mas_x[i + 1]))
    
    m = n - 1
    for i in range(1, n):
        matrix.append([])
        for j in range(0, m):
            matrix[i].append(((matrix[i - 1][j] - matrix[i - 1][j + 1]))/(mas_x[j] - mas_x[j + 2]))     
        m -= 1

    y = mas_y[0]
    fact = 1
    for i in range(0, n):
        fact *= (x - mas_x[i])
        y += matrix[i][0] * fact
    return y

if __name__ == "__main__":
    main();
