import pickle
import os
op = 0
m = 0
#------------------------СОЗДАТЬ------------------------------
def new_baze():
    mass1 = []
    baza1 = input('Введите название новой баззы данных - ')
    if baza1=='':
        print('Некорректный ввод')
    else:
        baza1+='.txt'
        with open(baza1,'wb') as file:
            pickle.dump(mass1,file)
        file.close()
        print('Новая база данных создана')
    if m==0:
        mennu(2)
    elif m==1:
        mennu(baza)
#----------------------ОТКРЫТЬ------------------------    
def open_baze():
    global baza
    baza = input('Введите какую базу данных открыть - ')
    baza+='.txt'
    if os.path.isfile(baza):
        with open(baza,'rb') as file:
            lines = pickle.load(file)
        print('База данных открыта')
        global op
        op = 1
        
    else:
        print('Нет такого файла')
    global m
    m = 1
    mennu(baza)

#------------------ПОСМОТРЕТЬ-----------------------        
def view_baze(baza):
    if op==1:
        with open(baza,'rb') as file:
            print('Марка            год выхода         цена')
            lines = pickle.load(file)
            for line in lines:
                q1 = line.get('s1')
                q2 = line.get('s2')
                q3 = line.get('s3')
                print('{:20s}{:20s}{:20s}'.format(q1,q2,q3))
        
        

    else:
        print('База данных не открыта')
    mennu(baza)
#----------------------ДОБАВИТЬ----------------------------
def add_baze(baza):
    w1 = w2 = 0
    dob = '1'
    if op==1:
        with open(baza,'rb') as file:
            mass3 = []
            mass3 = pickle.load(file)
            while dob!='2':
                add1 = input('Марка - ')
                while w1!=1:
                    add2 = input('Введите год выхода - ')
                    if add2.isdigit():
                        w1 = 1
                    else:
                        print('Неверная дата')
                        w1 = 0
                while w2!=1:
                    add3 = input('Цену - ')
                    if add3.isdigit():
                        w2 = 1
                    else:
                        print('Неккоректная сумма')
                        w2 = 0
                slov2 = dict(s1=add1,s2=add2,s3=add3)
                mass3.append(slov2)
                with open(baza,'wb') as file:
                    pickle.dump(mass3,file)
                print('*Добавлено*')
                dob = input('Добавить еще?     1 - да ,  2 - нет ')
                if dob=='1':
                    w1 = w2 = 0
        
    else:
        print('База данных не открыта')
    mennu(baza)
#-------------------------ПОИСК---------------------------
def search(baza):
    g1 = g2 = p1 = 0
    if op==1:
        while p1!=1:
            poisk = input('Поиск по (1)марке и году или (2)по дате выхода и цене - ')
            if poisk=='1':
                find1 = input('Введите марку - ')
                find4 = int(input('С какого года - '))
                with open(baza,'rb') as file:
                    mass4 = []
                    mass4 = pickle.load(file)
                    print('Марка           год выхода         цена')
                    for i in mass4:
                        if find1==i.get('s1') and find4<=int(i.get('s2')):
                            k1 = i.get('s1')
                            k2 = i.get('s2')
                            k3 = i.get('s3') 
                            print('{:20s}{:20s}{:20s}'.format(k1,k2,k3))
                            g1 = 1
                    if g1==0:
                        print('Авто не найдено')
                p1 = 1
            elif poisk=='2':
                find2 = input('Введите дату выхода авто - ')
                find3 = int(input('Введите с какой цены показать - '))
                with open(baza,'rb') as file:
                    mass4 = []
                    mass4 = pickle.load(file)
                    print('Марка           год выхода         цена')
                    for i in mass4:
                        if find2==i.get('s2') and find3<=int(i.get('s3')):
                            k1 = i.get('s1')
                            k2 = i.get('s2')
                            k3 = i.get('s3')
                            print('{:20s}{:20s}{:20s}'.format(k1,k2,k3))
                            g2 = 1
                    if g2==0:
                        print('Авто не найдено')
                p1 = 1
            else:
                print('Ошибка ввода')
                p1 = 0
        mennu(baza)            
    else:
        print('База данных не открыта')
        mennu(2)
#--------------------------УДАЛИТЬ------------------------------
def delete(baza):
    g1 = g2 = p2 = 0
    if op==1:
        while p2!=1:
            poisk = input('Удаление по (1)названию фильма или (2)по дате выхода и кассовым сборам - ')
            if poisk=='1':
                find1 = input('Введите название фильма - ') 
                with open(baza,'rb') as file:
                    mass4 = []
                    mass4 = pickle.load(file)
                for i in mass4:
                    if find1==i.get('s1'):
                        mass4.remove(i)
                        with open(baza,'wb') as file:
                            pickle.dump(mass4,file)
                        g1 = 1
                        print('*Удалено*')
                if g1==0:
                    print('фильм не найден')
                p2 = 1
                    
            elif poisk=='2':
                find2 = input('Введите дату выхода фильма - ')
                find3 = input('Введите кассовые сборы - ')
                with open(baza,'rb') as file:
                    mass4 = []
                    mass4 = pickle.load(file)
                for i in mass4:
                    if find2==i.get('s2') and find3==i.get('s3'):
                        mass4.remove(i)
                        with open(baza,'wb') as file:
                            pickle.dump(mass4,file)
                        print('*Удалено*')
                        g2 = 1
                if g2==0:
                    print('Фильм не найден')
                p2 = 1
            else:
                print('Ошибка ввода')
                p2 = 0
        mennu(baza)
    else:
        print('База данных не открыта')
        mennu(2)
#---------------------МЕНЮ-------------------------------                        
def mennu(baza):
    menu = 123
    while menu!='0':
        print()
        print('1 - создать   2 - открыть   3 - посмотреть    4 - добавить')
        print('5 - поиск   0 - завершить')
        menu = input()
        if menu=='1' or menu=='2' or menu=='3' or menu=='4' or menu=='5' or menu=='6':
            if menu=='1':
                new_baze()
            if menu=='2':
                open_baze()
            if menu=='3' and op==1:
                view_baze(baza)
            if menu=='3' and op==0:
                view_baze(1)
            if menu=='4' and op==1:
                add_baze(baza)
            if menu=='4' and op==0:
                add_baze(1)
            if menu=='5' and op==1:
                search(baza)
            if menu=='5' and op==0:
                search(1)
            if menu=='6' and op==1:
                delete(baza)
            if menu=='6' and op==0:
                delete(1)
        elif menu!='0':
            print('Ошибка ввода')
    print('*завершено*')
mennu(2)

