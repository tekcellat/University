from math import *
from prettytable import PrettyTable
#for install prettytable - open consol and :pip3 install prettytable

def func(x):
    return x*x

def main():
    table = PrettyTable([" N ", " X ", " Y "])
    table1 = PrettyTable([" N ", " X ", " Y "])
   
    mas_x = []
    mas_y = []
    matrix = []
    tmp_x = []
    tmp_y = []

    beg = - 100
    end = 101
    for i in range(beg, end):
        tmp_x.append(i)
        tmp_y.append(func(i))

    for i in range(0, len(tmp_x)):
        table1.add_row([i + 1, round(tmp_x[i], 5), round(tmp_y[i], 5)])
    print(table1, "\n")

    n = int(input("input n: "))
    x = float(input("input x: "))
    
    if (x <= beg):
        for i in range(0, n + 1):
            mas_x.append(tmp_x[i])
            mas_y.append(tmp_y[i])
    elif (x >= end - 1):
        for i in range(len(tmp_x) - (n + 1), len(tmp_x)):
            mas_x.append(tmp_x[i])
            mas_y.append(tmp_y[i])
    else:
        j = 0
        back = 0
        up = 0
        for i in range(1, abs(end - beg)):     
            if((tmp_x[j] <= x) & (tmp_x[i] > x)):
                up = i; back = j
                for k in range(0, n + 1):
                    if (k % 2 == 0):
                        if (up < len(tmp_x)):
                            mas_x.append(tmp_x[up])
                            mas_y.append(tmp_y[up])
                            up += 1
                        elif (back >= 0):
                            mas_x.insert(0, tmp_x[back])
                            mas_y.insert(0, tmp_y[back])
                            back -= 1
                    else:
                        if (back >= 0):
                            mas_x.insert(0, tmp_x[back])
                            mas_y.insert(0, tmp_y[back])
                            back -= 1
                        elif(up < len(tmp_x)):
                            mas_x.append(tmp_x[up])
                            mas_y.append(tmp_y[up])
                            up += 1
            j += 1
    
              
    for i in range(0, n + 1):
        table.add_row([i + 1, round(mas_x[i], 5), round(mas_y[i], 5)])
    
    
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
    
    print(table, "\n_____________")
    
    
    for i in range(0, n):
        print("\ny(x", (i + 2), "): ")
        for j in range(0, len(matrix[i])):
            print(round(matrix[i][j], 5))
        

    print("_____________\n")    
    print("\nYour  y = ", y)
    print("True  y = ", func(x))
    print("Error y = ", abs(abs(func(x)) - abs(y)))
           

if __name__ == "__main__":
    main();
