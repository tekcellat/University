from math import sin
def f(x):
    return sin(x) + x*x
ltc=('\u250c')
rtc=('\u2510')
hl=('\u2500')
vl=('\u2502')
spd=('\u252C')
spu=('\u2534')
llc=('\u2514')
rlc=('\u2518')
plus=('\u253C')
spr=('\u251C')
spl=('\u2524')
eps=input('Введите точность: ')
n1=input('Введите N1: ')
n2=input('Введите N2: ')
while not eps.replace('.','').replace('e-','').replace('e','').isdigit():
    print('Неверно введена точность!')
    exit()
while not int(n1):
    print('Ошибка ввода N1!')
    exit()
while not int(n2):
    print('Ошибка ввода N2!')
    exit()
topline=ltc+hl*(17)+spd+hl*(13)+spd+hl*(13)+rtc
midline=spr+hl*(17)+plus+hl*(13)+plus+hl*(13)+spl
lowline=llc+hl*(17)+spu+hl*(13)+spu+hl*(13)+rlc
s=i=0
step=100/n1
while i<100:
    s+=f((2*i+step)/2)
    i+=step
res=s*step
print(topline)
print(vl,' '*6,'Метод',' '*6,vl,' '*6,'N1',' '*5,vl,' '*6,'N2',' '*5,vl,sep='')
print(midline)
print(vl,' '*4,'Срединных',' '*4,vl,' ','{:11.4f}'.format(res),' ',end=vl,sep='')
s=i=0
step=100/n2
while i<100:
    s+=f((2*i+step)/2)
    i+=step
res=s*step
print(' ','{:11.4f}'.format(res),' ',vl,sep='')
print(vl,' прямоугольников ',vl,' '*13,vl,' '*13,vl,sep='')
print(midline)
s=s1=i=0
while i<=49:
    s+=f(2*i)
    s1+=f(2*i+1)
    i+=100/n1
s*=2
s1*=4
res=100*(f(0)+s+s1+f(100))/(n1*3)
print(v1,' '*5,'Парабол',' '*5,vl,' ','{:11.4f}'.format(res),' ',end=vl,sep='')
s=s1=i=0
while i<=49:
    s+=f(2*i)
    s1+=f(2*i+1)
    i+=100/n2
s*=2
s1*=4
res=100*(f(0)+s+s1+f(100))/(n2*3)
print(' ','{:11.4f}'.format(res),' ',vl,sep='')
print(lowline)
i1=100*(f(0)+f(100))/3
i2=100*(f(0)+2*f(50)*4(f(49))+f(100))/6
n2=2
while i2-i1>eps:
    n2+=1
    s=s1=i=0
    while i<=50:
        s+=f(2*i)
        s1+=f(2*i+1)
        i+=100/n2
    s*=2
    s1*=4
    i2=100*(f(0)+s+s1+f(100))/(n2*3)
print('Количество разбиений равно ',n2,', результат:\n',i2,sep='')
