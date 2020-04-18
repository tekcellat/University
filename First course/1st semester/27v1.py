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


for i in range(n1):
    print('Введите ',i+1,'-й элемент 1-го массива:',sep='')
    a1[i]=input()
    atmp=a1[i].replace('-','')
    if i<2:
        while not atmp.replace('.','').isdigit():
            print('Ошибка ввода, еще раз введите ',i+1,'-й элемент 1-го массива:',sep='')
            a1[i]=input()
            atmp=a1[i].replace('-','')
        if i==1:            
            rise=float(atmp)>a1[0]
    else:
        while not (atmp.replace('.','').isdigit() and rise==float(atmp)>a1[i-1]):
            print('Ошибка ввода, еще раз введите ',i+1,'-й элемент 1-го массива:',' ',rise,' ',float(atmp)>a1[i-1],' ',atmp.replace('.','').isdigit(),sep='')
            a1[i]=input()
            atmp=a1[i].replace('-','')
    a1[i]=float(a1[i])
for i in range(n2):
    print('Введите ',i+1,'-й элемент 2-го массива:',sep='')
    a2[i]=input()
    atmp=a2[i].replace('-','')
    if i<2:
        while not atmp.replace('.','').isdigit():
            print('Ошибка ввода, еще раз введите ',i+1,'-й элемент 2-го массива:',sep='')
            a2[i]=input()
            atmp=a2[i].replace('-','')
        if i==1:            
            rise=float(atmp)>a2[0]
    else:
        while not (atmp.replace('.','').isdigit() and rise==float(atmp)>a2[i-1]):
            print('Ошибка ввода, еще раз введите ',i+1,'-й элемент 2-го массива:',sep='')
            a2[i]=input()
            atmp=a2[i].replace('-','')
    a2[i]=float(a2[i])
res=[]
if n1>1 and a1[1]>a1[0] or n2>1 and a2[1]>a2[0]:
    # По возрастанию
    while n1 or n2:
        if n1:
            if n2:
                min1=min(a1)
                min2=min(a2)
                if min1<min2:
                    res.append(min1)
                    a1.remove(min1)
                    n1-=1
                else:
                    res.append(min2)
                    a2.remove(min2)
                    n2-=1
            else:
                res.append(min1)
                a1.remove(min1)
                n1-=1
        else:
            if n1:
                min1=min(a1)
                min2=min(a2)
                if min1<min2:
                    res.append(min1)
                    a1.remove(min1)
                    n1-=1
                else:
                    res.append(min2)
                    a2.remove(min2)
                    n2-=1
            else:
                res.append(min2)
                a2.remove(min2)
                n2-=1
else:
    # По убыванию
    while n1 or n2:
        if n1:
            if n2:
                max1=max(a1)
                max2=max(a2)
                if max1>max2:
                    res.append(max1)
                    a1.remove(max1)
                    n1-=1
                else:
                    res.append(max2)
                    a2.remove(max2)
                    n2-=1
            else:
                res.append(max1)
                a1.remove(max1)
                n1-=1
        else:
            if n1:
                max1=max(a1)
                max2=max(a2)
                if max1>max2:
                    res.append(max1)
                    a1.remove(max1)
                    n1-=1
                else:
                    res.append(max2)
                    a2.remove(max2)
                    n2-=1
            else:
                res.append(max2)
                a2.remove(max2)
                n2-=1
            
if len(res):
    print(res)
else:
    print('Массив не содержит элементов')
