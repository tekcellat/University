x = float(input("X = "))
y = float(input("Y = "))

if x > 0 and y > 0:
    print("1 - четверть")
elif x < 0 and y > 0:
    print("2 - четверть")
elif x < 0 and y < 0:
    print("3 - четверть")
elif x > 0 and y < 0:
    print("4 - четверть")
elif x == 0 and y > 0:
    print("Находится на линии абцисс")
elif x == 0 and y < 0:
    print("Находится на линии абцисс")
elif x < 0 and y == 0:
    print("Находится на линии ординат")
elif x > 0 and y == 0:
    print("Находится на линии ординат")
elif x == 0 and y == 0:
    print("Начало координат")
