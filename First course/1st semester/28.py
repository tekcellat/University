# Поиск совершенных чисел в массиве
# i - счетчик, n -  размер массива, f - логический флаг
n=input('Введите размер массива:')
while not n.isdigit():
    n=input('Ошибка ввода, еще раз введите размер массива:')
n=int(n)
a=[0]*n

# Ввод с одновременной проверкой правильности
for i in range(n):
    print('Введите ',i+1,'-й элемент:',sep='')
    a[i]=input()
    atmp=a[i].replace('-','')
    while not atmp.replace('.','').isdigit():
        print('Ошибка ввода, еще раз введите ',i+1,'-й элемент:',sep='')
        a[i]=input()
        atmp=a[i].replace('-','')
    a[i]=float(a[i])
print('Совершенные числа:')

# Флаг отсутствия совершенных чисел
f=True 
for i in a:
    if i-int(i)==0: # Совершенные числа всегда целые
        i=round(i)
        s=0
        for j in range(1,i):
            if i%j==0:
                print(j,end=' ')
                s+=j
        print(',',s)
        if s==i:
            f=False
            print(i,'- совершенное')
if f:
    print('Отсутствуют')
