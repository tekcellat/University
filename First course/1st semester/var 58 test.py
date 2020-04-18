n = int(input(" "))
S = 0
a = list(map(int,input(" ").split()))
#A massiv
for i in range(-n,0):
  S+=a[i]
for i in range(-n,0):
    if a[i] <= S/n:
        print(" ",a[i])
