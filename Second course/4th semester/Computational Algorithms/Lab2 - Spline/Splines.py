from math import sin
from prettytable import PrettyTable

def function(x):
    return x*x

# Building a spline:
def create_spline(x, y):
    table_size = len(x)

    # Initializing Spline Arrays:
    splines = [[0] * 5 for i in range(table_size)]

    for i in range(0, table_size):
        for j in range(2):
            splines[i][j] = x[i]           # adding x value for system of linear algebraic equations
            splines[i][j] = y[i]           # adding a coefficient for system of linear algebraic equations

    # The system of linear algebraic equations solution for spline
    # coefficients c[i] by the sweep method for tridiagonal matrices
    alpha = [0 for i in range(table_size - 1)]
    beta = [0 for i in range(table_size - 1)]
    A, B, C, F, Z = 0, 0, 0, 0, 0
    for i in range(1, table_size - 1):
        first_neighbor = x[i] - x[i - 1]
        second_neighbor = x[i + 1] - x[i]
        A = first_neighbor
        B = second_neighbor
        C = 2 * (first_neighbor + second_neighbor)
        F = 6 * ((y[i + 1] - y[i]) / second_neighbor - (y[i] - y[i - 1]) / first_neighbor)
        Z = A * alpha[i - 1] + C
        alpha[i] = -B / Z
        beta[i] = (F - A * beta[i - 1]) / Z

    splines[table_size - 1][3] = (F - A * beta[table_size - 2]) / (C + A * alpha[table_size - 2])

    # Finding a solution through reverse stroke of the sweep method:
    for i in range(table_size - 2, 0, -1):
        splines[i][3] = alpha[i] * splines[i + 1][3] + beta[i]

    # By the known coefficients c[i], we find the values of b[i] and d[i]:
    for i in range(table_size - 1, 0, -1):
        first_neighbor = x[i] - x[i - 1]
        splines[i][4] = (splines[i][3] - splines[i - 1][3]) / first_neighbor
        splines[i][2] = first_neighbor * (2 * splines[i][3] + splines[i - 1][3]) / 6 + (y[i] - y[i - 1]) / first_neighbor

    return splines

# Calculation of interpolation at a point:
def interpolation_in_point(x, splines):
    length = len(splines)

    if (x <= splines[0][0]):
        result = 1

    elif (x >= splines[length - 1][0]):
        result = length - 1

    else:
        i = 0
        j = length - 1
        while (i + 1 < j):

            k = int(i + (j - i) / 2)

            if (x <= splines[k][0]):
                j = k
            else:
                i = k
        result = j

    dx = x - splines[result][0]

    return splines[result][1] + (splines[result][2] + (splines[result][3] / 2 + splines[result][4] * dx / 6) * dx) * dx

# Table generation:
def create_table(left, right, step, function):
    x = []
    y = []

    # Adding x and y values in array:
    while left <= right:
        x.append(left)
        y.append(function(left))
        left += step

    return [x, y]

# Input data:
left_limit = float(input('Enter value of left limit: \n'))
right_limit = float(input('Enter value of right limit: \n'))
step = float(input('Enter step value: \n'))

x_column, y_column = create_table(left_limit, right_limit, step, function)

# Print table:
table_data = PrettyTable()
table_data.add_column('X', x_column)
table_data.add_column('Y(X)', y_column)
print(table_data)

splines = create_spline(x_column, y_column)

x = float(input('Enter x value: \n'))

print('\n ----- Results ----- \n')
print('Interpolation: ', interpolation_in_point(x, splines))
print('Exact value: ', function(x))
