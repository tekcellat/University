def removeWord(text):
    '''Удаление заданного слова из текста.'''
    word_to_remove = input("Введите слово, которое нужно удалить: ")
    text = text.replace(word_to_remove,' ')
    return text

def changeWord(text):
    '''Замена одного слова другим.'''
    old = input("Введите слово, которое нужно заменить: ")
    new = input("Введите слово, на которое нужно заменить предыдущее: ")
    text = text.replace(old,new)
    return text

def formatLeft(text):
    '''Выравнивание по левой стороне.'''
    for i in range(len(text)):
        text = text.lstrip()
    return text

def formatCenter(max_len, text):
    '''Выравнивание по ширине.'''
    for i in range(len(text)):
        text = text.center(max_len)
    return text

def formatRight(max_len, text):
    '''Выравнивание по правой стороне.'''
    new_text = []
    for i in range(len(text)):
        al = max_len(text) - len(text)
        new_line = text.replace(text, al * " " + text)
        new_text.append(new_line)
    return text

def printMenu():
    '''Вывод меню.'''
    print('МЕНЮ:\n 1)Удалить слово из текста.\n 2)Заменить одно слого другим.\
\n 3)Отформатировать текст по левому краю.\n 4)Отформатировать текст по \
правому краю.\n 5)Отформатировать текст по ширине.\n 6)Выход из программы.')

def printText(text):
    '''Вывод текста.'''
    print(text)

text = '''Это маленькое предложение для лабы
Написали меня кое-как дабы,
Работала программа,и была сдала лаба
Далее будет самая длинная строка,
Яблоко, груша, варенье, помидор, банан, майонез
И при таком завтраке тебе быстро настанет конец.'''
max_len=0
print(text)

while True:
    printMenu()
    ask = input('Введите цифру, соответствующую вашему запросу: ')
    if ask == '1':
        text = removeWord(text)
        printText(text)
    elif ask == '2':
        text = changeWord(text)
        printText(text)
    elif ask == '3':
        text = formatLeft(text)
        printText(text)
    elif ask == '4':
        text = formatRight(max_len, text)
        printText(text)
    elif ask == '5':
        text = formatCenter(max_len, text)
        printText(text)
    elif ask == '6':
         exit()
    else:
        print('ВЫ ВВЕЛИ НЕВЕРНЫЙ ЗАПРОС!!!\n\n')
        pass
    
