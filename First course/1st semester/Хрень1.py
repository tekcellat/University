while True:
      n = input('n: ')
      if n.isdigit() and n[0] != '0':
            n = int(n)
            break
      else:
            print('Вы должны ввести целое, положительное число.')

mas = []
i = 0
while i < n:
      flag = 0
      numOfMin = 0
      numOfDot = 0
      t = str(input('mas[' + str(i) + ']: '))
      for j in range(len(t)):
            if t[j] == '-':
                  if numOfMin == 1:
                        flag = 1
                  numOfMin = 1
            elif t[j] == '.':
                  if numOfDot == 1:
                        flag = 1
                  numOfDot = 1
            elif not t[j].isdigit():
                  flag = 1
      if flag == 0:
            i += 1
            mas.append(float(t))
      else:
            print('Вы должны ввести число.')

s = 0
flagInd = 1
ind = -1
for i in range(n):
      if mas[i] > 0 and flagInd:
            ind = i
            flagInd = 0
      if i % 3 == 0 and mas[i] < 0:
            s += mas[i]

if ind == -1:
      print('В массиве нет положительных элементов.')
else:
      mas[ind] = s
      print(mas)
            
      
