n = int(input('n: '))
a = [[float(i) for i in input().split()] for j in range(n)]

maxOfP = maxOfM = 0
indP = indM = 0
for i in range(n):
      numP = numM = 0
      for j in range(n):
            if a[j][i] > 0:
                  numP += 1
            if a[i][j] < 0:
                  numM += 1
      if numP > maxOfP:
            maxOfP = numP
            indP = i
      if numM > maxOfM:
            maxOfM = numM
            indM = i

print()
print('Исходная матрица:')
for i in range(n):
      for j in range(n):
            print('{:10.2f}'.format(a[i][j]), end=' ')
      print()
      
if maxOfP == 0:
      print('В массиве нет положительных элементов.')
elif maxOfM == 0:
      print('В массиве нет отрицательных элементов.')
else:
      for i in range(n):
            a[i][indP], a[indM][i] = a[indM][i], a[i][indP]
      a[indM][indP] = 0

      print()
      print('Полученая матрица:')
      for i in range(n):
            for j in range(n):
                  print('{:10.2f}'.format(a[i][j]), end=' ')
            print()
