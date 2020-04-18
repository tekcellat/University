from math import sin, pi, factorial, cos, exp, log
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
from prettytable import PrettyTable

def phi(first_point, second_point):
    return first_point ** second_point

# Table generation:
def creating_table(file_name):

    input_file = open(file_name, 'r')

    table_data = PrettyTable()
    data = []

    for line in input_file:
        if line:
            x, y, w = map(float, line.split())
            data.append(Table(x, y, w))

    table_data.add_column('Source Table', data)

    print(table_data)

    input_file.close()

    return data

# Finding the coefficient of the approximating function:
def finding_coefficient(table, degree):

    SLAU, column_of_free = creating_SLAU(table, degree)

    inverse_SLAU = inverse_matrix(SLAU)

    multiplication_result = multiplication(column_of_free, inverse_SLAU)

    return multiplication_result

def creating_SLAU(table, polynomial_degree):

    table_size = len(table)

    SLAU = [[0 for i in range(0, polynomial_degree + 1)] for j in range(0, polynomial_degree + 1)]
    column_of_free = [0 for i in range(0, polynomial_degree + 1)]

    for m in range(0, polynomial_degree + 1):
        for i in range(0, table_size):
            buffer = table[i].w * phi(table[i].x, m)

            for k in range(polynomial_degree + 1):
                SLAU[m][k] += buffer * phi(table[i].x, k)
            column_of_free[m] += buffer * table[i].y

    return SLAU, column_of_free

# To obtain the inverse matrix:
def inverse_matrix(matrix):

    matrix_size = len(matrix)

    result = [[0 for i in range(0, matrix_size)] for j in range(0, matrix_size)]

    for i in range(0, matrix_size):
        column = for_column(matrix, i)
        for j in range(0, matrix_size):
            result[j][i] = column[j]

    return result

# To convert a matrix into an inverse matrix:
# (I SO MISS NUMPY):
def for_column(our_matrix, column):

    matrix_size = len(our_matrix)
    mega_matrix = [[our_matrix[i][j] for j in range(matrix_size)] for i in range(matrix_size)]
    new_column = [0 for i in range(matrix_size)]

    for i in range(matrix_size):
        mega_matrix[i].append(float(i == column))

    for i in range(0, matrix_size):
        if mega_matrix[i][i] == 0:
            for j in range(i + 1, matrix_size):
                if mega_matrix[j][j] != 0:
                    mega_matrix[i], mega_matrix[j] = mega_matrix[j], mega_matrix[i]
        for j in range(i + 1, matrix_size):
            d = - mega_matrix[j][i] / mega_matrix[i][i]
            for k in range(0, matrix_size + 1):
                mega_matrix[j][k] += d * mega_matrix[i][k]

    for i in range(matrix_size - 1, -1, -1):
        for_result = 0
        for j in range(matrix_size):
            for_result += mega_matrix[i][j] * new_column[j]
        new_column[i] = (mega_matrix[i][matrix_size] - for_result) / mega_matrix[i][i]

    return new_column

# Multiplication of SLAU to column:
def multiplication(column, SLAU):

    column_size = len(column)
    result = [0 for j in range(column_size)]

    for j in range(column_size):
        for k in range(column_size):
            result[j] += column[k] * SLAU[j][k]

    return result

def print_result(table, result, polynomial_degree):

    dx = 10

    if len(table) > 1:
        dx = (table[1].x - table[0].x)

    # For approximating function:
    x = np.linspace(table[0].x - dx, table[-1].x + dx, 100)
    y = []
    for i in x:
        buffer = 0
        for j in range(polynomial_degree + 1):
            buffer += phi(i, j) * result[j]
        y.append(buffer)

    plt.plot(x, y)

    x_initial = [a.x for a in table]
    y_initial = [a.y for a in table]


    plt.plot(x_initial, y_initial, 'kD', color = 'green', label = '$Source$')

    plt.grid(True)
    plt.legend(loc = 'best')

    min_y = min(min(y), min(y_initial))
    max_y = max(max(y), max(y_initial))
    dy = (max_y - min_y) * 0.03

    plt.axis([table[0].x - dx, table[-1].x + dx, min_y - dy, max_y + dy])

    plt.show()
    return

Table = namedtuple('Data', ['x','y', 'w'])

our_table = creating_table('zero_test.txt')

polynomial_degree = int(input('Enter the degree of a polynomial: \n'))

result = finding_coefficient(our_table, polynomial_degree)
print_result(our_table, result, polynomial_degree)
