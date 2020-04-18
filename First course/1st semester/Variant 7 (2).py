n = int(input("Введите количество элементов в массиве А: "))
#kolicestvo
S = 0
count = 0
a = list(map(int,input("Введите элементы массива А: ").split()))
#A massiv
for i in range(n):
  if a[i] > 0:
    S+=a[i]
    count+=1

if count==0:
  print('В заданном массиве отсуствуют положительные элементы')
else:
  print(" ",S/count)
