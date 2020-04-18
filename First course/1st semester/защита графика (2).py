#Какурин ИУ7-15
#Защита: график


#print('график: x^2+x-6')
#a = float(input('Введите значение а: '))
#b = float(input('Введите значение b: '))
#h = float(input('Введите шаг: '))



    
min_x = float(input('Введите начальное значение: '))
max_x = float(input('Введите конечное значение: ' )) 
step = float(input('Шаг вывода значений функций: '))
    
x = min_x
miny = x*x+x-6
maxy = x*x+x-6
n = 1
summ = 0
while True:
    x = float('{:.4f}'.format(x))

    y1 = x*x+x-6
            

    if y1>0:

        summ+=y1
    if miny > y1:
        miny = y1
    if maxy < y1:
        maxy = y1
    
    #print("шаг\|{}\t|{:10.4f}\t|{:10.4f}\t|" .format (n,x,y1))  

    x += step
    n += 1
    if x>max_x+0.0001:
        break
print('\n\nПостроение графика y1=x^2+x-6')
print('\nМинимальное значение y1: {:.4f}'.format(miny))
print('Максимальное значение y1: {:.4f}'.format(maxy))

    
    
zero = round((0 - miny)/(maxy - miny)*49 + 1)
print(zero)
print('        {:.2f}                                              {:.2f}'
          .format(miny,maxy))
print('    x     +------------------------------------------------+')
if zero > 0 and maxy >= 0 and miny <= 0:
    print('         ',end='')
    print(' ' * zero + '0')
       

x = min_x 

while True:
    x = float('{:.4f}'.format(x))
    y = x*x+x-6
    n_dop =(y-miny)/(maxy-miny)*49 + 1
        
    if n_dop%1 >= 0.5:
        n = n_dop//1+1
        n = int(n)
            
    else:
        n = int(n_dop)


            
    if x>=0:
        print('  {:6.4f} '.format(x),end='')
    else:
        print(' {:6.4f} '.format(x),end='')

    
    zero = abs(zero)
    rast1 = n - zero - 1
    rast2 = zero - n - 1
            
            
    if n < zero:
        print(' ' * n + '*' + ' ' * rast2 + '|' )
                
    elif n > zero:
        print(' ' * zero + '|' + ' ' * rast1 + '*')
                  
    else:
        print(' ' * zero + '*' )
                
    x += step
            
            
    if x > max_x + 0.001:
        break



