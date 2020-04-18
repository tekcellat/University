import random
Arr = []
def arrgen(Arr):
    sep = str(input('Input any symbol: '))
    alp = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    while True:
        if sep in alp:
            print('Dont use a letters! ')
            sep = str(input('Write symblos again : '))
        else:
            break
    for i in range(5):
        B = []
        for i in range(4):
            B.append(alp[random.randint(0,len(alp)-1)])
        Arr.append(B)

    for i in Arr:
        i.insert(random.randint(1,4),sep)
    return sep
sep = arrgen(Arr)

for i in Arr:
    print(i)

def arrsort(Arr, sep):
    alp1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alp2 = 'abcdefghijklmnopqrstuvwxyz'
    C = []
    D = []
    for i in range(len(Arr)):
        n = 0
        N = 0
        for j in range(0,Arr[i].index(sep)):
            if Arr[i][j] in alp2:
                n += 1
            if Arr[i][j] in alp1:
                N += 1
        C.append(n)    
        D.append(N)
    print(C)
    print(D)
    F = []
    for i in range(len(C)):
        if D[i] < C[i]:
            pass
        else:
            F.append(Arr[i])
    for i in F:
        print(i)
arrsort(Arr, sep)
