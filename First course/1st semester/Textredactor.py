# abc - согласные буквы, text - текст(вау),choice - выбор действия,
# rech -выбор выравнивания, остальные переменные - рабочие
#                                                  Иванов ИУ7-11Б
abc=['б','в','г','д','ж','з','й','к','л','м','н','п','р',
     'с','т','ф','х','ц','ч','ш','щ']
text=['Пусть мама','услышит, пусть','мама придет;',
'Съешь же ещё этих','мягких французских булок','да выпей чаю;',
      'А эти','предложения созданы','просто чтобы быть.']
def word_remove():# Удаляет введенную фразу
    remword=input('Введите слово для удаления:')
    i=0
    f=True
    while i<len(remword) and f:
        lord=ord(remword[i].lower())
        if not(lord>=ord('а') and lord<=ord('я') or remword[i].lower()=='ё'):
            f=False
        i+=1
    if f:
        for i in range(len(text)):
            wordlist=text[i].split(' ')
            j=0
            m=len(wordlist)
            while j<m:
                tmpword=wordlist[j]
                l=0
                n=len(tmpword)
                while l<n:
                    lord=ord(tmpword[l].lower())
                    if not(lord>=ord('а') and lord<=ord('я')
                    or tmpword.lower()=='ё'):
                        tmpword=tmpword.replace(tmpword[l],'')
                        n-=1
                        l-=1
                    l+=1
                if tmpword==remword:
                    text[i]=text[i].replace(remword,'')
                    j-=1
                    m-=1
                j+=1
    else:
        print('Неверный ввод, ожидалось слово')
def word_replace(): # Заменяет введенную фразу
    remword=input('Введите заменяемое слово:')
    i=0
    f=True
    while i<len(remword) and f:
        lord=ord(remword[i].lower())
        if not(lord>=ord('а') and lord<=ord('я') or remword[i].lower()=='ё'):
            f=False
        i+=1
    if f:
        newword=input('Введите слово-заменитель:')
        i=0
        while i<len(newword) and f:
            lord=ord(newword[i].lower())
            if not(lord>=ord('а') and lord<=ord('я') or newword[i].lower()=='ё'):
                f=False
            i+=1
        if f:
            for i in range(len(text)):
                wordlist=text[i].split(' ')
                j=0
                m=len(wordlist)
                while j<m:
                    tmpword=wordlist[j]
                    l=0
                    n=len(tmpword)
                    while l<n:
                        lord=ord(tmpword[l].lower())
                        if not(lord>=ord('а') and lord<=ord('я')
                        or tmpword.lower()=='ё'):
                            tmpword=tmpword.replace(tmpword[l],'')
                            n-=1
                            l-=1
                        l+=1
                    if tmpword==remword:
                        text[i]=text[i].replace(remword,newword)
                        j-=1
                        m-=1
                    j+=1
        else:
            print('Неверный ввод, ожидалось слово')
    else:
        print('Неверный ввод, ожидалось слово')
def print_text():# Выводит текст. используется несколько раз
    if rech==1:
        for i in text:
            print(i)
    else:                
        maxlen=len(text[0])
        for i in text:
            if len(i)>maxlen:
                maxlen=len(i)
        if rech==2:
            for i in text:
                print((maxlen-len(i))*' ',i)
        elif rech==3:
            for i in text:
                spc=(maxlen-len(i))//2
                print(spc*' ',i,(maxlen-spc//2)*' ')
        elif rech==4:
            for i in text:
                wordlist=i.split(' ')
                num=len(wordlist)-1
                if num:
                    spc=(maxlen-len(i))//num
                    spl=(maxlen-len(i))%num
                    k=0
                    for j in wordlist:
                        print(j,spc*' ',end='')
                        if spl:
                            print(end=' ')
                            spl-=1
                    print()
                else:
                    print(i)
choice=1
rech=1
for i in text:
    print(i)
print()
while choice>0:
    print('0. Выйти\n1. Изменить текст\n2. Удалить фразу\n3. Заменить фразу\n',
          '4. Выровнять текст\n5. Вывести текст\n',
          '6. Найти слово с максимальным количеством согласных букв\n',sep='')
    choice=input()
    while not(choice.isdigit()) or int(choice)<0 or int(choice)>6:
        print('Ошибка, повторите ввод')
        choice=input()
    choice=int(choice)
    
    if choice:# Если введен 0, ничего не делаем
        if choice==1:
            i=0
            f=True
            text=[]
            while f:
                print('Введите',i+1,'-ю строку:')
                string=input()
                if len(string):
                    text.append(string)
                    i+=1
                    f=(string[-1]!='.')
                else:
                    f=False
            print_text()
        elif len(text):# Если текст пустой, операции над ним не имеют смысла
            if choice==2:
                word_remove()
            elif choice==3:
                word_replace()
            elif choice==4:
                print('Как выровнять текст?\n1.По левому краю\n',
                      '2.По правому краю\n3.Центрировать\n4.По ширине',sep='')
                rech=input()
                while not(rech.isdigit()) or int(rech)<1 or int(rech)>4:
                    print('Ошибка, повторите ввод')
                    rech=input()
                rech=int(rech)
            elif choice==5:
                print_text()
            elif choice==6:
                maxcl=0
                imax=0
                num=0
                for i in range(len(text)):
                    c=0
                    for j in text[i]:
                        f=True
                        k=0
                        while f and k<21:
                            if abc[k]==j.lower():
                                c+=1
                                f=False
                            k+=1
                        else:
                            jnum=ord(j.lower())
                            if not (jnum>=ord('а') and jnum<=ord('я')
                            or j=='ё'):
                                if c>maxcl:
                                    maxcl=c
                                    imax=num
                                c=0
                    if c>maxcl:
                        maxcl=c
                        imax=num
                    num+=1
                print(imax+1,'-е предложение содержит искомое слово\n')
        else:
            print('Текст остсутствует')
    print()
