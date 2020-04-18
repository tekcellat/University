n = int(input('Количество элементов матрицы= '))
def my(matr):
    if len(matr) == 0 or len(matr) == 1 :
        print('Неверная длина матрицы' ,end=' ')
    else:
    def mtrx(matrix,ii,jj):
        res = []
        k = 0
        p = 0
        for i in range(len(matrix)):
            if i != ii:
                res.append([])
                for j in range(len(matrix)):
                    if j != jj:
                        res[k].append(matrix[i][j])
                k += 1   
        return res

            for i in matr:
                print(i)
    print('Сама матрица')
    print('\nD = {}'.format(my(matr)))
