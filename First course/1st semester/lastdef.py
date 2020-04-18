a = [(i) for i in input().split()]
 
alpha = [] # массив индексов
b = [] # итоговый массив
i = 0
j = 0
buf = 0
while i<len(a):
    if i in alpha:
        continue
    else:        
        bul_test = a[i] in a[i+1:] 
        if bul_test:
            j = i+1
            alpha.append(i)
            b.append(a[i])
            while j<len(a):
                if a[j] == a[i]:
                    alpha.append(j)
                j+=1
    i+=1
    
print(b)
