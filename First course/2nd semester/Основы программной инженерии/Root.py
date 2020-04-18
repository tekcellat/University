import math
a = int(input("Введите значение a= "))
b = int(input("Введите значение b= "))
c = int(input("Введите значение c= "))
D = b ** 2 - 4 * a * c
print(D)
if D < 0:
  print("Корней нет")
elif D == 0:
  x = -b / 2 * a
  print (x)
else:
  x1 = (-b + math.sqrt(D)) / (2 * a)
  x2 = (-b - math.sqrt(D)) / (2 * a)
  print(x1)
  print(x2)
