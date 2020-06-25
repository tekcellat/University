from math import *
import matplotlib.pyplot as plt
import numpy as np

print('Программа для уточнения корней методом <Итераций>\n')
print('Исходные значения:')

a = float(input('Введите левый конец интервала: '))
b = float(input('Введите правый конец интервала: '))
h = float(input('Введите шаг: '))
Eps = float(input('Введите точность (Eps): '))
MAXiterations = 100            #Максимальное число итераций

def f(x): return(x*sin(x))       # Функция       
def f1(x): return(sin(x)+x*cos(x))     # 1я Производная функции
def f2(x): return(2*cos(x)-x*sin(x))     # 2я Производная функции
def f3(x): return(-3*sin(x)-x*cos(x))     # 3я Производная функции
def Fi(x,k,F):return(x-k*F(x)) # Преобразованная ф-я


def f4(x): return(x**2-2*x-3)                #1-я функция
def f5(x): return(sin(x))                         #2-я функция
def Function1(x): return(x**2-2*x-3-sin(x))  #разность функций
def Function2(x): return(2*x-2-cos(x))  #1-я производная разности функций
##-------------
    
def RootIterations(F,F1):  
   lamda = []    # Коэффициент
   interval = [] # Интервал
   an = a
   interval.append(an)
   while an+0.0001 <= b:  #дробление отрезка
      an+=h
      if an<=b:
          interval.append(an)
   m=[]
   for i in range(1,len(interval)):      # Нахождение коэффициентов
      m.clear()
      n = (interval[i]-interval[i-1])/10   
      for k in range(10):
          m.append(F1(interval[i-1] + k*n))
      maxx = max(m)    
      minn = min(m)
      max2 = max(abs(maxx) , abs(minn))
      if abs(maxx) == max2: lamda.append(maxx)
      else:  lamda.append(minn)
      
   global root,keys,num_iter,A,B,Func
   root = []      # корни
   keys = []      # код ошибки
   num_iter=[]    # количество итераций
   A=[]; B=[]     # начало и конец отрезка содержащий корень
   Func=[]        # значение функции в корне
   for i in range(1,len(interval)):
      key = '-'
      iterations = 1
      if F(interval[i-1])*F(interval[i]) <= 0:    #проверка на наличие корней        
         x0 = interval[i-1]
         x = Fi(x0, 1/(lamda[i-1]),F)      
        
         while abs(x0 - x) > Eps:
             p = 0
             x0 = x            
             x = Fi(x0, 1/(lamda[i-1]),F)
             iterations += 1
             if iterations >= MAXiterations:       # проверка на перебор итераций
                key = '0'
                break
         if F==f:
             A.append(interval[i-1])
             B.append(interval[i])
             keys.append(key)
             num_iter.append(iterations)
             
         root.append(x0)        
         Func.append(f(x0))

def RootIterations1(F,F1):  
   lamda = []    # Коэффициент
   interval = [] # Интервал
   an = a+h
   interval.append(an)
   while an+0.0001 <= b-h:  #дробление отрезка
      an+=h
      if an<=b:
          interval.append(an)
   m=[]
   for i in range(1,len(interval)):      # Нахождение коэффициентов
      m.clear()
      n = (interval[i]-interval[i-1])/10   
      for k in range(10):
          m.append(F1(interval[i-1] + k*n))
      maxx = max(m)    
      minn = min(m)
      max2 = max(abs(maxx) , abs(minn))
      if abs(maxx) == max2: lamda.append(maxx)
      else:  lamda.append(minn)
      
   global root,keys,num_iter,A,B,Func
   root = []      # корни
   keys = []      # код ошибки
   num_iter=[]    # количество итераций
   A=[]; B=[]     # начало и конец отрезка содержащий корень
   Func=[]        # значение функции в корне
   for i in range(1,len(interval)):
      key = '-'
      iterations = 1
      if F(interval[i-1])*F(interval[i]) <= 0:    #проверка на наличие корней        
         x0 = interval[i-1]
         x = Fi(x0, 1/(lamda[i-1]),F)      
        
         while abs(x0 - x) > Eps:
             p = 0
             x0 = x            
             x = Fi(x0, 1/(lamda[i-1]),F)
             iterations += 1
             if iterations > MAXiterations:       # проверка на перебор итераций
                key = '0'
                break
         if F==f:
             A.append(interval[i-1])
             B.append(interval[i])
             keys.append(key)
             num_iter.append(iterations)
             
         root.append(x0)        
         Func.append(f(x0))
print('''
***О Программе!***
Номер ошибки:
        Если "0" : корень не сошелся за максимальное количество итераций
        Если "-" : корень сошелся за максимальное количество итераций
      ''')

#Таблица
RootIterations(f,f1)
print('Результат работы программы: ')
print('----------------------------------------------------------------------------------------------------')
print('|№ корня |  A  |   B  |  корень(х) |f(x) |Число ит| Ошибка |')
print('----------------------------------------------------------------------------------------------------')
for i in range(len(keys)):
  print('|'+'{:8}'.format(i+1)+'|'+\
      '{:5.3}'.format(A[i])+'|'+'{:6.3}'.format(B[i])+\
         '|'+'{:12.5}'.format(root[i])+'|'+'{:11.0e}'.format(Func[i])+\
           '|'+'{:14}'.format(num_iter[i])+'|   '+'{:5}'.format(keys[i])+'|')
  print('-------------------------------------------------------------------------')  

#График
if len(root)!=0:
  # plt.figure(1)
   x = np.linspace(a,b,1000)
   y = np.sin(x)                                    # Функция F
   plt.plot(x,x*y,'r',linewidth=3,label = 'F(x)')
   plt.grid(True)
   plt.title('$F(x)$')
   plt.xlabel('x'); plt.ylabel('y')
   plt.plot(root, Func, 'ko',label = '$Корни$')     # Kорни
   RootIterations1(f1,f2)                            # вызов ф-ии для экстремума  
   plt.plot(root, Func, 'yo',label = '$Экстремум$')
   StackY =[]
   StackX = []
   Stack = []
   a3 = a
   Fstack=[]
   while a3<b:
       Stack.append(a3)
       a3+=0.001
   for i in range(len(Stack)):
       Fstack.append(f(Stack[i]))
       
   StackY.append(min(Fstack))
   uu = Fstack.index(min(Fstack))
   StackX.append(Stack[uu])
   
   plt.plot(StackX,StackY,'bo',label ='$Мин-фу$')

   
   StackY.clear()
   StackX.clear()
          
   StackY.append(max(Fstack))
   uu = Fstack.index(max(Fstack))
   StackX.append(Stack[uu])
   
   plt.plot(StackX,StackY,'mo',label ='$Макс-фу$')
   
   RootIterations1(f2,f3)                            # вызов ф-ии для перегиба
   plt.plot(root, Func, 'cs',label = '$Перегиб$')  
   plt.legend(loc='upper left')
   plt.show()   
else:
   print("ERROR: на интервале нет корней, удоволетворяющих условию!")
   
###################ЧАСТЬ НОМЕР 2###################   
RootIterations(Function1,Function2)
Fnewroot = []                         #Y Точек пересечения
for i in range(len(root)):
   Fnewroot.append(f4(root[i]))
if len(root)!=0:
   x = np.linspace(a,b,1000)                                  
   plt.plot(x,x**2-2*x-3,'r',linewidth=3,label = 'x^2-2x-3')
   plt.plot(x,np.sin(x),'g',linewidth=3,label = 'sin(x)')
   plt.grid(True)
   plt.xlabel('x'); plt.ylabel('y')
   plt.plot(root, Fnewroot, 'ko',label = '$Корни$') # корни
   plt.legend(loc='upper left')
plt.show()
