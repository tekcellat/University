# Объединение двух упорядоченных масивов в один
# i,j,k - счетчики, n1,n2 - размеры массивов, a1,a2 - массивы, res -
# результирующий массив
n1=input('Введите размер 1-го массива:')
while not n1.isdigit():
    n1=input('Ошибка ввода, еще раз введите размер 1-го массива:').split()
n2=input('Введите размер 2-го массива:')
while not n2.isdigit():
    n2=input('Ошибка ввода, еще раз введите размер 2-го массива:').split()
n1,n2=int(n1),int(n2)
a1=[0]*n1
a2=[0]*n2

# Ввод обоих массивов с параллельной проверкой правильности
for i in range(n1):
    print('Введите ',i+1,'-й элемент 1-го массива:',sep='')
    a1[i]=input()
    atmp=a1[i].replace('-','')
    while not (atmp.replace('.','').isdigit() and (float(atmp)>=a1[i-1])):
        print('Ошибка ввода, еще раз введите ',i+1,'-й элемент 1-го массива:',sep='')
        a1[i]=input()
        atmp=a1[i].replace('-','')
    a1[i]=float(a1[i])
for i in range(n2):
    print('Введите ',i+1,'-й элемент 2-го массива:',sep='')
    a2[i]=input()
    atmp=a2[i].replace('-','')
    while not (atmp.replace('.','').isdigit() and (float(atmp)>=a2[i-1])):
        print('Ошибка ввода, еще раз введите ',i+1,'-й элемент 2-го массива:',sep='')
        a2[i]=input()
        atmp=a2[i].replace('-','')
    a2[i]=float(a2[i])
    
i=j=k=0
res=[0]*(n1+n2)
# Массивы упорядочены, сравниваем соответствующие элементы
while i<n1+n2:
    if j<len(a1):
        if k<len(a2):
            if a1[j]<a2[k]:
                res[i]=a1[j]
                j+=1
            else:
                res[i]=a2[k]
                k+=1
        else:
            res[i]=a1[j]
            j+=1
    else:
        if k<len(a2):
            res[i]=a2[k]
            k+=1
    i+=1
    
if len(res):
    print(res)
else:
    print('Массив не содержит элементов')
