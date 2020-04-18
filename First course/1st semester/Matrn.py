n = int(input('Введите размер матрицы: ' ))
print('Введите матрицу по', '{:d}'.format(n), 'элемента(ов) в строке.')
a = [[float(j) for j in input().split()] for i in range(n)]

# Поиск столбца с наибольшим количеством отрицательных элементов и
# элементов, находящихся ниже главной диагонали.
maxNum = 0
masUnder = []
for i in range(n):
      num = 0
      for j in range(n):
            if a[j][i] < 0:
                  num += 1
            if i < j:
                  masUnder.append(a[j][i])
      if num > maxNum:
            maxNum = num
            ind = i

print()
print('Исходная матрица:')
for i in range(n):
      for j in range(n):
            print('{: 5.2f}'.format(a[i][j]), end =' ')
      print()
print()
if maxNum == 0:
      print('В матрице нет отрицательных элементов.')
else:
      print('Номер столбца с наибольшим количеством отрицательных элементов: '\
            + '{:d}'.format(ind+1))
print()
if masUnder:
      print('Массив элементов, находящихся под главной диагональю:')
      for i in range(len(masUnder)):
            print('{:.3f}'.format(masUnder[i]), end = ' ')
else:
      print('Под главной диагональю нет элементов.')
            
