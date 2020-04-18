b = map(int(input('Введите количество элементов в матрице')))
if b <4:
    print('dont E matric')
elif b == 4:
    x1,y1 = map(int(input('1ya stroka').split( )))
    x2,y2 = map(int(input('2ya stroka').split( )))
    D=x1*y2-x2*y1
    print('Opred matrix',D)
