a = [int(x) for x in input("a = ").split()]

def isPol(mas):
    for i in range(len(mas) // 2):
        j = len(mas) - i - 1
        if a[i] != a[j]:
            return False
    return True

res = []
for i in range(len(a) - 1):
    j = len(a) - 1
    while j > i:
        mas = a[i:j + 1:]
        if isPol(mas.copy()):
            if len(mas) > len(res):
                res = mas.copy()
        j -= 1

print(res)
        
