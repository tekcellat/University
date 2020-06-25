


import random
n = int(input("Вводите количество чисел в массиве: "))
a = []
b = [0]
c = [0]
for i in range(n):
    m = random.randint(-100,100)
    a.append(m)
    b.append(m)
    c.append(m)
for i in range(1,len(b)):
    if b[i-1] > b[i]:
        b[0] = b[i]
        j = i - 1
        while b[j] > b[0]:
            b[j+1] = b[j]
            j = j - 1
        b[j+1] = b[0]
for i in range(1,len(c)):
    if c[i-1] < c[i]:
        c[0] = c[i]
        j = i - 1
        while c[j] < c[0]:
            c[j+1] = c[j]
            j = j - 1
        c[j+1] = c[0]
del b[0]
del c[0]
print("-----------------------------------------------")
print(a)
print("-----------------------------------------------")
print(b)
print("-----------------------------------------------")
print(c)
print("-----------------------------------------------")























