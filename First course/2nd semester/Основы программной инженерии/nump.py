from random import random
import numpy

def create_matrix():
    file = 'matrix.txt'
    f = open(file, 'w')
    N = 3
    M = 3
    mtx = []
    arr = [None] * N*M

    for i in range(N):
        a = []
        for j in range(M):
            a.append(int(random()*9))
        mtx.append(a)
    for i in range(N):
        for j in range(M):
            print("%3d" % mtx[i][j], end='')
        print()
    with open(file, 'a') as f:
        f.write("%s" % mtx)
    if( mtx[1][0] == 0 and mtx[2][0] == 0 and mtx[2][1] == 0 or mtx[0][1] == 0 and mtx[0][2] == 0 and mtx[1][2] == 0):
        print("Triangle matrix")
    else:
        print("Not triangle matrix")
    numpy.linalg.det(mtx)
    if numpy.linalg.det == 0:
        print('Not virojdennaya')
    else:
        print('Virojdennaya')
        
def print_menu():
    print(' 1) Create')
    print(' 2) Close')

while True:
    print_menu()
    ask = input('Which you want: ')
    if ask == '1':
        create_matrix()
    elif ask == '2':
        break
    else:
        print('Please input again')
