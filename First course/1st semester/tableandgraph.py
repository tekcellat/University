from math import sqrt
ltc=('\u250c')
rtc=('\u2510')
hl=('\u2500')
vl=('\u2502')
spd=('\u252C')
spu=('\u2534')
llc=('\u2514')
rlc=('\u2518')
plus=('\u253C')
#######
x0,step,xn=map(float,
               input('Введите начальное значение, шаг и конечное значение:').
               split())
if xn>x0 and step<0 or step==0 or xn<x0 and step>0:
    print('Неверно введен шаг')
else:
    x=x0
    xmax=8
    ymax1=ymax2=4
    y1=[]
    y2=[]
    if step>0:
        cond = (x<=xn)
    else:
        cond = (x>=xn)
    while cond:
        if xmax<len(str('{:9.4f}'.format(x))):
            xmax=len(str('{:9.4f}'.format(x)))
        func1=x*2**x-1.05
        func1=round(func1,4)
        if x<=-1:
            func2=('-')
        else:
            func2=sqrt(x+1)-1/(x+1)
            func2=round(func2,4)
            if len(str(func2))>ymax2:
                ymax2=len(str(func2))
        if len(str(func1))>ymax1:
            ymax1=len(str(func1))
        y2.append(func2)
        y1.append(func1)
        x+=step
        if step>0:
            cond = (x<=xn)
        elif step<0:
            cond = (x>=xn)
        else: cond=False
    if step:
        maxnum=max(5,len(str(int((xn-x0+1)/step))))
    else:
        maxnum=5
    topline=ltc+hl*(maxnum+2)+spd+hl*(xmax+2)+spd+hl*(ymax1+2)+spd+hl*(ymax2+2)+rtc
    lowline=llc+hl*(maxnum+2)+spu+hl*(xmax+2)+spu+hl*(ymax1+2)+spu+hl*(ymax2+2)+rlc
    print(topline)
    print(vl,'Номер',vl,'%-*s'%(xmax,'Аргумент'),vl,'%-*s'%(ymax1,'phi1'),vl,'%-*s'%(ymax2,'phi2'),vl)
    x=x0
    num=0
    if step>0:
        cond = (x<=xn)
    else:
        cond = (x>=xn)
    while cond:
        func1=str(y1[num])
        func2=str(y2[num])
        num+=1
        print(vl,'%-*s'%(maxnum,num),vl,'%-*s'%(xmax,'{:9.4f}'.format(x)),vl,'%-*s'%(ymax1,func1),vl,'%-*s'%(ymax2,func2),vl)
        x+=step
        if step>0:
            cond = (x<=xn)
        else:
            cond = (x>=xn)
    print(lowline)
#######
    miny=min(y1)
    maxy=max(y1)
    print('Минимальное значение 1-й функции равно','{:8.4f}'.format(miny))
    if miny==maxy:
        miny=min(0,miny)
        maxy=max(maxy,0)
    d=(maxy-miny)/60
    if maxy<0 or miny>0:
        zero=False
    else:
        zero=True
        if d:
            y0=round(-miny/d)
        else:
            y0=0
    y=y1
    y1.sort()
    i=0
    j=0
    print(' '*xmax,end='')
    while i<61:
        if zero and i==round(y0):
            print(0, end=' ')
            i+=2
            while j+1<len(y1) and i>round((y1[j]-miny)/d):
                j+=1
        elif i==round((y1[j]-miny)/d):
            el=round(y1[j],4)
            if not zero or i < y0 - len(str(el)) - 2 or i > y0 + 1:
                print(el,end=' ')
                i+=len(str(el))+1
            else:
                while(i!=y0):
                    print(end=' ')
                    i+=1
            while j+1<len(y1) and i>round((y1[j]-miny)/d):
                j+=1
        else:
            print(end=' ')
            i+=1
    print()
    j=0
    i=0
    print(' '*xmax,end='')
    while i<61:
        if zero and i==round(y0):
            print(plus,end=hl)
            i+=2
            while j+1<len(y1) and i>round((y1[j]-miny)/d):
                j+=1
        elif i==round((y1[j]-miny)/d):
            if not zero or i<y0-len(str(round(y1[j],4)))-2 or i>y0+1:
                print(end=spu)
                print(hl*(len(str(round(y1[j],4)))),end='')
                i+=len(str(round(y1[j],4)))+1
            else:
                while(i!=y0):
                    print(end=hl)
                    i+=1
            while j+1<len(y1) and i>round((y1[j]-miny)/d):
                j+=1
        else:
            print(end=hl)
            i+=1
    print('>Y')
    x=x0
    for j in range(num):
        print('{:9.4f}'.format(x),end='')
        i=0
        while i<61:
            if i==round((y[j]-miny)/d):
                print(end='*')
            elif zero and i==y0:
                print(end=vl)
            else:
                print(end=' ')
            i+=1
        x+=step
        print()
    print(' '*xmax,end='')
    if zero:
        for i in range(y0):
            print(' ',end='')
        print('\u02C5','X')
