import re

def isOK(a):
      f = 0
      for x in range(len(a)-1):
            if a[x] <= a[x+1]:
                  f+=1
            else:
                  return False
      return True

while True:
      n = input('Количество элементов: ')
      if re.search(r'^\s*[+-]?\d+\s*$', n):
            n = int(n)
            break
      else:
            print('Введите положительное целое число.')

mas = []
i = 0
while i < n:
      t = input('mas['+str(i)+']: ')
      if re.search(r'^\s*[+-]?\d*.?\d+\s*$', t) or\
         re.search(r'^\s*[+-]?\d+e?[+-]?\d+\s*$', t) or\
         re.search(r'^\s*[+-]?\d+.?\d*\s*$', t):
            mas.append(float(t))
            i += 1

mas2 = []
for i in range(n):
      k = 14
      t = mas[i]
      while not(float.is_integer(t)):
            t = round(t, k)
            k -= 1
            t *= 10
      t = int(t)
      mas2.append(str(t))

for i in range(n):
      if float.is_integer(mas[i]):
            mas[i] = int(mas[i])

num = 0
for i in range(n-1):
      if isOK(mas2[i]):
            mas3 = [str(mas[i])]
            k = 0
            for j in range(n):
                  if isOK(mas2[j]) and i!=j:
                        if  j > i:
                              if (int(mas3[k][-1]) <= int(mas2[j][0])):
                                    num += 1
                                    mas3.append(mas2[j])
                                    s = str(num) + ') '
                                    for g in range(len(mas3)):
                                          s += str(mas3[g]) + ' '
                                    print(s)
                        else:
                              if int(mas3[k][0]) >= int(mas2[j][-1]):
                                    num += 1
                                    mas3.insert(k, mas2[j])
                                    k += 1
                                    s = str(num) + ') '
                                    for g in range(len(mas3)):
                                          s += str(mas3[g]) + ' '
                                    print(s)

print('Количество последовательностей: ', num)
            
      
            
